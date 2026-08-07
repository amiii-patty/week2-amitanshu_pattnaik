
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
    product, category_name = result
    product.category_name = category_name
    return product


def search_products(db: Session, name: str = None, category_id: int = None):
    query = (
        db.query(Product, Category.category_name)
        .join(Category, Product.category_id == Category.category_id)
    )
    if name:
        query = query.filter(Product.product_name.ilike(f"%{name}%"))
    if category_id:
        query = query.filter(Product.category_id == category_id)
    return _map_results(query.all())


def delete_product(db: Session, product_id: int):
    product = (
        db.query(Product)
        .filter(Product.product_id == product_id)
        .first()
    )
    if product:
        db.delete(product)
        db.commit()
    return product


def _map_results(results):
    products = []
    for product, category_name in results:
        product.category_name = category_name
        products.append(product)
    return products