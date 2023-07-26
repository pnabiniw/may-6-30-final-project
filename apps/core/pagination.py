class CustomPagination:
    start = 0
    limit = 6

    def get_last_page(self, view):
        quotient = view.get_queryset().count() / self.limit
        if isinstance(quotient, float):
            last_page = int(quotient) + 1
        else:
            last_page = quotient
        return last_page

    def get_pagination_indexes(self, view):
        page_number = view.request.GET.get("page")
        if page_number is not None:
            try:
                page_number = int(page_number)
            except ValueError:
                return self.start, self.limit
            last_page = self.get_last_page(view)
            if page_number > last_page:
                page_number = last_page
            return (self.limit*(page_number-1), self.limit*page_number) if page_number > 0 else (self.start, self.limit)
        return self.start, self.limit

    def get_paginated_qs(self, view):
        start, end = self.get_pagination_indexes(view)
        return view.get_queryset()[start: end]

    @staticmethod
    def get_current_page(view):
        page = view.request.GET.get('page')
        default_active = "one"
        if page is not None:
            try:
                page = int(page)
            except ValueError:
                return 1, default_active
            if page <= 0:
                return page, "prev"
            if page > 3:
                return page, "next"
            else:
                mapper = {1: "one", 2: "two", 3: "three"}
                return page, mapper[page]
        return 1, default_active

    @staticmethod
    def get_nested_pagination(qs, nested_size): # [obj1, obj2, obj3, obj4]
        all_data = []
        each_data = list()
        for index, each in enumerate(qs, start=1):
            each_data.append(each)
            if index % nested_size == 0:
                all_data.append(each_data)
                each_data = list()
        if each_data:
            all_data.append(each_data)
        return all_data  # [[obj1, obj2], [obj3, obj4]]
