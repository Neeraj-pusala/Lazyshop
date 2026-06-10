from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")


# ---------- Models ----------
class CartItem(BaseModel):
    product_id: str
    name: str
    image: str
    category: str
    original_price: float
    quantity: int


class OrderCreate(BaseModel):
    student_id: str
    year_label: str
    discount_percent: int
    items: List[CartItem]
    subtotal: float
    discount_amount: float
    total: float


class Order(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    student_id: str
    year_label: str
    discount_percent: int
    items: List[CartItem]
    subtotal: float
    discount_amount: float
    total: float
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ---------- Product Catalog (seed) ----------
PRODUCTS = [
    # Hostel Essentials
    {"id": "he-1", "name": "Cotton Bed Sheet (Single)", "category": "Hostel Essentials", "original_price": 599,
     "image": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=600&q=80&auto=format&fit=crop",
     "description": "Soft cotton single bed sheet, perfect for hostel beds."},
    {"id": "he-2", "name": "Memory Foam Pillow Cover", "category": "Hostel Essentials", "original_price": 299,
     "image": "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=600&q=80&auto=format&fit=crop",
     "description": "Plush pillow cover with breathable fabric."},
    {"id": "he-3", "name": "Electric Glass Kettle 1.5L", "category": "Hostel Essentials", "original_price": 1499,
     "image": "https://images.unsplash.com/photo-1594032194509-0056023973b2?w=600&q=80&auto=format&fit=crop",
     "description": "Quick-boil electric kettle for instant noodles and tea."},
    {"id": "he-4", "name": "Ceramic Coffee Mug Set", "category": "Hostel Essentials", "original_price": 449,
     "image": "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=600&q=80&auto=format&fit=crop",
     "description": "Set of 2 minimalist ceramic mugs."},
    {"id": "he-5", "name": "Foldable Storage Box", "category": "Hostel Essentials", "original_price": 799,
     "image": "https://images.unsplash.com/photo-1591129841117-3adfd313e34f?w=600&q=80&auto=format&fit=crop",
     "description": "Collapsible storage for clothes and books."},
    {"id": "he-6", "name": "LED Study Desk Lamp", "category": "Hostel Essentials", "original_price": 899,
     "image": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=600&q=80&auto=format&fit=crop",
     "description": "Eye-care LED lamp with adjustable brightness."},
    {"id": "he-7", "name": "Wall Hook Organizer", "category": "Hostel Essentials", "original_price": 249,
     "image": "https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=600&q=80&auto=format&fit=crop",
     "description": "Adhesive wall hooks for towels and bags."},
    {"id": "he-8", "name": "Bath Towel - Premium", "category": "Hostel Essentials", "original_price": 399,
     "image": "https://images.unsplash.com/photo-1620626011761-996317b8d101?w=600&q=80&auto=format&fit=crop",
     "description": "Ultra-soft 100% cotton bath towel."},

    # Stationery
    {"id": "st-1", "name": "A5 Hardcover Notebook", "category": "Stationery", "original_price": 249,
     "image": "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=600&q=80&auto=format&fit=crop",
     "description": "200-page ruled notebook with premium binding."},
    {"id": "st-2", "name": "Gel Pen Pack (10)", "category": "Stationery", "original_price": 199,
     "image": "https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?w=600&q=80&auto=format&fit=crop",
     "description": "Smooth-writing 0.5mm gel pens, blue ink."},
    {"id": "st-3", "name": "Wooden Pencil Set", "category": "Stationery", "original_price": 149,
     "image": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=600&q=80&auto=format&fit=crop",
     "description": "Premium HB graphite pencils, pack of 12."},
    {"id": "st-4", "name": "Sticky Notes Multi-Color", "category": "Stationery", "original_price": 129,
     "image": "https://images.unsplash.com/photo-1517842645767-c639042777db?w=600&q=80&auto=format&fit=crop",
     "description": "5 colors, 100 sheets each for fast revision."},
    {"id": "st-5", "name": "Geometry Box", "category": "Stationery", "original_price": 349,
     "image": "https://images.unsplash.com/photo-1452860606245-08befc0ff44b?w=600&q=80&auto=format&fit=crop",
     "description": "Complete math instrument set in a tin."},
    {"id": "st-6", "name": "Highlighter Markers (5)", "category": "Stationery", "original_price": 179,
     "image": "https://images.unsplash.com/photo-1568871391537-e3c925caf8d4?w=600&q=80&auto=format&fit=crop",
     "description": "Vibrant chisel-tip highlighters for notes."},
    {"id": "st-7", "name": "Desk Organizer Caddy", "category": "Stationery", "original_price": 599,
     "image": "https://images.unsplash.com/photo-1456735190827-d1262f71b8a3?w=600&q=80&auto=format&fit=crop",
     "description": "Wooden organizer for pens, clips and notes."},
    {"id": "st-8", "name": "Spiral Sketchbook A4", "category": "Stationery", "original_price": 299,
     "image": "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=600&q=80&auto=format&fit=crop",
     "description": "Thick paper, ideal for sketches and notes."},

    # Snacks
    {"id": "sn-1", "name": "Spicy Potato Chips", "category": "Snacks", "original_price": 50,
     "image": "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=600&q=80&auto=format&fit=crop",
     "description": "Crispy chips with bold masala flavor."},
    {"id": "sn-2", "name": "Dark Chocolate Bar", "category": "Snacks", "original_price": 199,
     "image": "https://images.unsplash.com/photo-1623876423842-1baadf456c5d?w=600&q=80&auto=format&fit=crop",
     "description": "70% cocoa, smooth and rich."},
    {"id": "sn-3", "name": "Instant Cup Noodles", "category": "Snacks", "original_price": 60,
     "image": "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=600&q=80&auto=format&fit=crop",
     "description": "Ready in 3 minutes — late night essential."},
    {"id": "sn-4", "name": "Cold Brew Coffee Can", "category": "Snacks", "original_price": 149,
     "image": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=600&q=80&auto=format&fit=crop",
     "description": "Smooth cold brew to power study sessions."},
    {"id": "sn-5", "name": "Roasted Almonds Pack", "category": "Snacks", "original_price": 249,
     "image": "https://images.unsplash.com/photo-1508061253366-f7da158b6d46?w=600&q=80&auto=format&fit=crop",
     "description": "Healthy roasted almonds, 200g."},
    {"id": "sn-6", "name": "Choco Chip Cookies", "category": "Snacks", "original_price": 89,
     "image": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=600&q=80&auto=format&fit=crop",
     "description": "Crunchy cookies loaded with chocolate."},
    {"id": "sn-7", "name": "Fruit Granola Bar", "category": "Snacks", "original_price": 45,
     "image": "https://images.unsplash.com/photo-1571748982800-fa51082c2224?w=600&q=80&auto=format&fit=crop",
     "description": "Oats, honey and dried fruit on-the-go."},
    {"id": "sn-8", "name": "Sparkling Lemon Drink", "category": "Snacks", "original_price": 80,
     "image": "https://images.unsplash.com/photo-1437418747212-8d9709afab22?w=600&q=80&auto=format&fit=crop",
     "description": "Refreshing fizzy citrus drink."},
]


# ---------- Routes ----------
@api_router.get("/")
async def root():
    return {"message": "Lazy Shop API"}


@api_router.get("/products")
async def get_products():
    return {"products": PRODUCTS}


@api_router.post("/orders", response_model=Order)
async def create_order(payload: OrderCreate):
    if not payload.items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    order = Order(**payload.model_dump())
    doc = order.model_dump()
    await db.orders.insert_one(doc)
    return order


@api_router.get("/orders/{student_id}")
async def get_orders(student_id: str):
    cursor = db.orders.find({"student_id": student_id}, {"_id": 0}).sort("created_at", -1)
    orders = await cursor.to_list(200)
    return {"orders": orders}


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
