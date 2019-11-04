from .crawler_manager import CrawlerManager
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import json

manager = CrawlerManager(0)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def run_crawler(request):
    data = request.data
    crawler_name = data['crawler_name']
    overlap_chk = data['overlap_chk']
    print("in run_crawler" + str(data))
    result = manager.run_crawler(crawler_name, overlap_chk)

    return Response(result)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def post_category(request):
    result = {'status': False}
    category = request.data['category']
    if category == 'category':
        result = {'category': manager.send_category_dic_and_info()}
    elif category == 'sub_category':
        result = {'sub_category': manager.send_sub_category_dic_and_info()}
    elif category == 'category_size_part':
        result = {'category_size_part': manager.send_category_size_part_dic_and_info()}
    elif category == 'sub_category_size_part':
        result = {'sub_category_size_part': manager.send_sub_category_size_part_dic_and_info()}

    return Response(result)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def post_category_dic_and_info(request):
    """
    :param request: 위 method 에서 전달한 list 를 바탕으로 사용자가 mapping 을 하게 되면, 선택한 정보를 받아와 직접 DB에 반영하는 method
    category: 어떠한 category(cate, sub_cate, cate_size_part 등...) 정보에 대해서 mapping 을 할 것인지
    info: dic 에 update 할 info 정보 (querySet 형태가 아닌 model 자체 정보가 넘와야 할듯 > 해당 info_pk 로 수정)
    dic: update 대상인 dic 의 정보 (querySet 형태가 아닌 model 자체 정보가 넘와야 할듯 > 해당 dic_pk 로 수정)
    :return:
    """
    result = {'status': False}
    try:
        category = request.data['category']
        info_pk = request.data['info_pk']
        dic_pk = request.data['dic_pk']
    except Exception:
        return Response(result)

    if category == 'category':
        result = manager.receive_category_dic_info(dic_pk, info_pk)
    elif category == 'sub_category':
        result = manager.receive_sub_category_dic_info(dic_pk, info_pk)
    elif category == 'category_size_part':
        result = manager.receive_category_size_part_dic_info(dic_pk, info_pk)
    elif category == 'sub_category_size_part':
        result = manager.receive_sub_category_size_part_dic_info(dic_pk, info_pk)

    return Response(result)

'''
{
    "category_dic_id": 30,
    "category_similar": "INNER WEAR",
    "category_info_id": null
}
{
    "category_info_id": 17,
    "category_name": "레그웨어/속옷"
}

'''