# from rest_framework import pagination
# from rest_framework.response import Response

# class CustomPagination(pagination.PageNumberPagination):
#     class CustomPagination(pagination.PageNumberPagination):
#         page_size = 10 # Default number of items per page (can be overridden in settings)
#         page_size_query_param = 'page_size'  # Allow the client to specify page size
#         max_page_size = 100
#     def get_paginated_response(self, data):
#         return Response({
#             'links': {
#                 'next': self.get_next_link(),
#                 'previous': self.get_previous_link()
#             },
#             'count': self.page.paginator.count,
#             'results': data
#         })




