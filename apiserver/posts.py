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
def get_postdetail(req):
    post_sets = models.PostTb.objects.filter(class_code=req['class_code'])
    res = []
    if post_sets.exists():
        for post in post_sets:
            temp_dict = {
                "post_id": post.post_id,  # pk
                "title": post.title,  # 제목
                "content": post.content,  # 내용
                "author_id": post.author_id,  # 작성자 id
                "create_date": post.create_date,  # 시간
                "hit": post.hit
            }
            res.append(temp_dict)
    return res

