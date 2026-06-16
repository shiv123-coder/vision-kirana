from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.api.deps import get_db, get_current_active_user, RoleChecker
from app.models.user import User, RoleEnum
from app.models.shop import Shop
from app.models.application import Application, ApplicationStatus
from app.schemas.shop import ShopRegistrationRequest, RegistrationResponse, ShopResponse, ShopDetailResponse, ShopUpdateRequest

router = APIRouter()

@router.post("/register", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
def register_shop(
    *,
    db: Session = Depends(get_db),
    shop_in: ShopRegistrationRequest,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Register a new shop and initiate a loan application.
    Accessible by SHOP_OWNER or LOAN_OFFICER.
    """
    
    # Create Shop
    new_shop = Shop(
        owner_id=current_user.id,
        name=shop_in.name,
        owner_name=shop_in.owner_name,
        mobile=shop_in.mobile,
        address=shop_in.address,
        city=shop_in.city,
        state=shop_in.state,
        category=shop_in.category,
        years_in_business=shop_in.years_in_business,
        monthly_sales=shop_in.monthly_sales
    )
    db.add(new_shop)
    db.flush() # Flush to get the shop ID
    
    # Create Application
    new_application = Application(
        shop_id=new_shop.id,
        status=ApplicationStatus.DRAFT,
        requested_amount=shop_in.requested_loan,
        purpose=shop_in.loan_purpose
    )
    db.add(new_application)
    
    try:
        db.commit()
        db.refresh(new_shop)
        db.refresh(new_application)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not complete registration")
        
    return {
        "shop": new_shop,
        "application_id": new_application.id
    }

@router.get("/", response_model=list[ShopResponse])
def get_user_shops(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get all shops for the current user.
    """
    shops = db.query(Shop).filter(Shop.owner_id == current_user.id).all()
    return shops

@router.get("/{shop_id}", response_model=ShopDetailResponse)
def get_shop(
    shop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get a specific shop by ID along with its applications.
    """
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    if shop.owner_id != current_user.id and current_user.role not in [RoleEnum.ADMIN, RoleEnum.LOAN_OFFICER]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return shop

@router.put("/{shop_id}", response_model=ShopDetailResponse)
def update_shop(
    shop_id: int,
    shop_in: ShopUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update a shop and potentially its latest draft application.
    """
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    if shop.owner_id != current_user.id and current_user.role not in [RoleEnum.ADMIN]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    # Update shop fields
    update_data = shop_in.model_dump(exclude_unset=True)
    
    # Extract application fields if any
    app_fields = {}
    for key in ["requested_loan", "loan_purpose"]:
        if key in update_data:
            app_fields[key] = update_data.pop(key)
            
    for field, value in update_data.items():
        setattr(shop, field, value)
        
    # Update draft application if needed
    if app_fields:
        # Find the latest draft application
        draft_app = next((app for app in shop.applications if app.status == ApplicationStatus.DRAFT), None)
        if draft_app:
            if "requested_loan" in app_fields:
                draft_app.requested_amount = app_fields["requested_loan"]
            if "loan_purpose" in app_fields:
                draft_app.purpose = app_fields["loan_purpose"]
        else:
            # If they provided app fields but there is no draft, we could create one or ignore.
            # Let's create one if we don't have an active one.
            pass

    db.add(shop)
    try:
        db.commit()
        db.refresh(shop)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not update shop")
        
    return shop
