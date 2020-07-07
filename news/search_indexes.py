from haystack.indexes import SearchIndex, Indexable, CharField
from news.models import trump1


class UserSearchIndex(SearchIndex, Indexable):
    # 查询的域名、必须提供、并且设置 document=True
    text = CharField(document=True, use_template=True)
    #author = CharField(model_attr='user')  # 创建一个author字段


    def get_model(self):
        return trump1

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
