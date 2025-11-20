import uvicorn 
from fastapi import FastAPI
from routes.authors import router as authors_router
from routes.books import router as books_router
from routes.customer import router as customer_router
from routes.genres import router as genres_router
from routes.loan import router as loan_router

app = FastAPI()


<<<<<<< HEAD
@app.get("/")
def read_root():
    return {
        "version": "1.1.0"
    }
=======
#@app.get("/")
#def read_root():
#    return {
#        "Hello": "World",
#        "version": "0.1.0"
#    }
>>>>>>> origin/mi-rama

app.include_router(authors_router)
app.include_router(books_router)
app.include_router(customer_router)
app.include_router(genres_router)
app.include_router(loan_router)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")