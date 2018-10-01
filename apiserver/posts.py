from . import models
def board_list(req):
    user_set = models.UserTb.objects.get(klas_id=req['id'])
    class_list = str(user_set.class_2018_2).split(',')
    class_list.pop()
    res = []
    print(class_list)
    for code in class_list:
        class_info=models.CourseTb.objects.get(class_code=code)
        temp_dict={
            "class_code" : code,
            "class_name" : class_info.class_name,#강의명
            "instructor" : class_info.instructor#강사이름
        }
        res.append(temp_dict)
    return res

def get_postlist(req):
    post_sets=models.PostTb.objects.filter(class_code=req['class_code'])
    res = []
    if post_sets.exists():
        for post in post_sets:
            temp_dict = {
                "post_id":post.post_id,#pk
                "title": post.title,#제목
                "content": post.content, #내용
                "author_id":post.author_id,#작성자 id
                "create_date":post.create_date,#시간
                "hit":post.hit
            }
            res.append(temp_dict)
    return res
def get_postdetail(pk):
    post = models.PostTb.objects.get(post_id=pk)
    res=[]
    temp_dict = {
                "type" : "0",#0 이면 게시글 본문
                "post_id": post.post_id,  # pk
                "title": post.title,  # 제목
                "content": post.content,  # 내용
                "author_id": post.author_id,  # 작성자 id
                "create_date": post.create_date,  # 시간
                "hit": post.hit
            }
    res.append(temp_dict)
    comment_sets=models.CommentTb.objects.filter(post_id=post.post_id)
    if comment_sets.exists(): # 존재할시
        for comment in comment_sets:
            temp_dict={
                "type" : "1", #1임으로 댓글띠
                "content" : comment.content,
                "create_date" : comment.create_date,
                "author_id": comment.author_id
            }
            res.append(temp_dict)
    return res

def comment_add(form,pk):
    obj=models.CommentTb(class_code=form.data['class_code'],
                         post_id=pk,
                         author_id=form.data['author_id'],
                         content=form.data['content'])
    obj.save()

def post_add(form):
    obj=models.PostTb(class_code=form.data['class_code'],
                         author_id=form.data['author_id'],
                         title=form.data['title'],
                         content=form.data['content'],
                         hit=0)
    obj.save()

def post_update(form,pk):
    post = models.PostTb.objects.get(post_id=pk)
    #post.class_code=form.data['class_code']
    #post.author_id = form.data['author_id'],
    post.title=form.data['title']
    post.content=form.data['content']
    post.save()

def post_delete(req,pk):
    try :
        post = models.PostTb.objects.get(post_id=pk)
        if post.author_id==req['id']:
            post.delete()
            return [{'STATUS': 'SUCCESS'}]
        else :
            return [{'STATUS': 'ACCESS FAIL'}]
    except models.PostTb.DoesNotExist:
        return [{'STATUS': 'NONE DATA'}]
