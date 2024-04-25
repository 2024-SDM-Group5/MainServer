from sqlalchemy.orm import Session
from app.models.dbModel import Comment
from app.schemas.comments import CommentCreate, CommentUpdate, NewComment, CommentResponse

def create_comment(db: Session, user_id: int, comment_data: CommentCreate) -> NewComment:
    db_comment = Comment(author=user_id, diary_id=comment_data.diaryId, content=comment_data.content)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return NewComment(id=db_comment.comment_id)

def update_comment(db: Session, user_id: int, comment_id: int, comment_data: CommentUpdate) -> NewComment:
    comment = db.query(Comment).filter(Comment.comment_id == comment_id).first()
    if comment:
        setattr(comment, "diary_id", comment_data.diaryId)
        setattr(comment, "content", comment_data.content)
        db.commit()
        db.refresh(comment)
    return NewComment(id=comment.comment_id)

def delete_comment(db: Session, user_id: int, comment_id: int) -> CommentResponse:
    comment = db.query(Comment).filter(Comment.comment_id == comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()
    return CommentResponse(success=True, message=f"User {user_id} deleted comment {comment_id}")