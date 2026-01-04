from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.db import products_collection
from app.schemas import ProductCreate, ProductOut, ProductUpdate

router = APIRouter()

def _doc_to_out(doc) -> ProductOut:
    return ProductOut(
        id=str(doc["_id"]),
        title=doc["title"],
        description=doc.get("description", ""),
        category=doc["category"],
        season=doc["season"],
        price_toman=doc["price_toman"],
        sizes=doc.get("sizes", []),
        colors=doc.get("colors", []),
        stock=doc.get("stock", 0),
        image_url=doc.get("image_url"),
    )

@router.post("", response_model=ProductOut)
async def create_product(payload: ProductCreate):
    col = products_collection()
    res = await col.insert_one(payload.model_dump())
    doc = await col.find_one({"_id": res.inserted_id})
    return _doc_to_out(doc)

@router.get("", response_model=list[ProductOut])
async def list_products(limit: int = 20, skip: int = 0):
    col = products_collection()
    cursor = col.find({}).skip(skip).limit(min(limit, 100))
    docs = await cursor.to_list(length=min(limit, 100))
    return [_doc_to_out(d) for d in docs]

@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: str):
    col = products_collection()
    try:
        oid = ObjectId(product_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid product id")
    doc = await col.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Product not found")
    return _doc_to_out(doc)

@router.put("/{product_id}", response_model=ProductOut)
async def update_product(product_id: str, payload: ProductUpdate):
    col = products_collection()
    try:
        oid = ObjectId(product_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid product id")
    update = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not update:
        doc = await col.find_one({"_id": oid})
        if not doc:
            raise HTTPException(status_code=404, detail="Product not found")
        return _doc_to_out(doc)
    await col.update_one({"_id": oid}, {"$set": update})
    doc = await col.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Product not found")
    return _doc_to_out(doc)

@router.delete("/{product_id}")
async def delete_product(product_id: str):
    col = products_collection()
    try:
        oid = ObjectId(product_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid product id")
    res = await col.delete_one({"_id": oid})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"status": "deleted"}

@router.get("/search/query", response_model=list[ProductOut])
async def search(q: str, season: str | None = None, category: str | None = None, limit: int = 20):
    col = products_collection()
    query = {"$or": [{"title": {"$regex": q, "$options": "i"}}, {"description": {"$regex": q, "$options": "i"}}]}
    if season:
        query["season"] = season
    if category:
        query["category"] = category
    cursor = col.find(query).limit(min(limit, 100))
    docs = await cursor.to_list(length=min(limit, 100))
    return [_doc_to_out(d) for d in docs]
