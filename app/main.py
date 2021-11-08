from fastapi import FastAPI, Response, status, HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel
from random import randrange

from starlette.status import HTTP_202_ACCEPTED

app = FastAPI()

my_posts = {
    1: {
        "content": "Demo post",
        "user_id": 4, 
        "jabs": 2,   
    },

    2: {
        "content": "Ed balls",
        "user_id": 1,
        "jabs": 3,
    }
}


class Post(BaseModel):
    content: str
    user_id: int
    jabs: int = 0


class PostContent(BaseModel):
    content: str


@app.get("/")
async def root():
    return {"message": "Hello world"}


@app.get("/posts")
def get_posts():
    return {"data": "post 1"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)

    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int):

    post = my_posts.get(id)

    if not post:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )
    
    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
    if id not in my_posts:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )

    my_posts.pop(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.patch("/posts/{id}", status_code=HTTP_202_ACCEPTED)
def update_post(id: int, post_content: PostContent):

    if id not in my_posts:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )
    
    my_posts[id]['content'] = post_content.dict().get('content')

    return {"message": "Updated successfully"}