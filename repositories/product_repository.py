
from sqlalchemy.orm import Session

from models.product import Product
from models.category import Category
from schemas import product_schema


def create_product(db: Session, request: product_schema.ProductCreate):
    new_product = Product(
        product_name=request.product_name,
        description=request.description,
        price=request.price,
        quantity=request.quantity,
        url=request.url,
        category_id=request.category_id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return get_product_by_id(db, new_product.product_id)


def get_product_by_name(db: Session, product_name: str):
    return db.query(Product).filter(Product.product_name == product_name).first()


def get_all_products(db: Session):
    results = (
        db.query(Product, Category.category_name)
        .join(Category, Product.category_id == Category.category_id)
        .all()
    )
    return _map_results(results)


def get_product_by_id(db: Session, product_id: int):
    result = (
        db.query(Product, Category.category_name)
        .join(Category, Product.category_id == Category.category_id)
        .filter(Product.product_id == product_id)
        .first()
    )
    if not result:
        return None
    # Fix: return a dict — Pydantic reads dicts cleanly, no ORM mutation needed
    product, category_name = result
    return _to_dict(product, category_name)

def search_products(db: Session, name: str = None, category_id: int = None):
    query = (
        db.query(Product, Category.category_name)
        .join(Category, Product.category_id == Category.category_id)
    )
    # Fix: "is not None" — guards against falsy values like 0 or ""
    if name is not None:
        query = query.filter(Product.product_name.ilike(f"%{name}%"))
    if category_id is not None:
        query = query.filter(Product.category_id == category_id)

    return _map_results(query.all())

# Fix: added update_product_quantity — fetches, updates, commits and returns full product with category
def update_product_quantity(db: Session, product_id: int, quantity: int):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        return None
    product.quantity = quantity
    db.commit()
    db.refresh(product)
    return get_product_by_id(db, product_id)

def _to_dict(product: Product, category_name: str) -> dict:
    return {
        "product_id": product.product_id,
        "product_name": product.product_name,
        "description": product.description,
        "price": product.price,
        "quantity": product.quantity,
        "url": product.url,
        "category_id": product.category_id,
        "category_name": category_name
    }


def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return product


def _map_results(results) -> list:
    if not results:
        return []
    return [_to_dict(product, category_name) for product, category_name in results]