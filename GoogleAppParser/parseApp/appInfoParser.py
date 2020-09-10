# -*- coding: utf-8 -*-

# app 세부 정보 파싱
class AppInfo:

    def app_name(self, bs_view):
        App_name_elem = bs_view.find('h1', class_='AHFaub')
        app_name = App_name_elem.text
        return app_name

    def review_score(self, bs_view):
        # review_score_avg
        # 리뷰 점수가 없는 경우에 리뷰 평점 및 점수를 0 처리한다.
        try:
            score_avg_elem = bs_view.find('div', class_='BHMmbe')
            review_score_info = score_avg_elem.text
            return review_score_info
        except:
            review_score_info = '0'
            return review_score_info


    def review_width(self, bs_view):
        # review 그래프의 width값 파싱
        try:
            review_width = {}
            review_num = {}
            width = bs_view.findAll('div', class_='mMF0fd')
            w = 0
            for width_cnt in width:
                w = w + 1
                review_style = width_cnt.findAll('span')[1]
                review_width[w] = review_style['style'][7:-1]
            for r in review_width:
                review_num[r] = int(review_width[r])
            return review_num[1], review_num[2], review_num[3], review_num[4], review_num[5]
        except:
            review_num[1] = 0
            review_num[2] = 0
            review_num[3] = 0
            review_num[4] = 0
            review_num[5] = 0
            return review_num[1], review_num[2], review_num[3], review_num[4], review_num[5]


    def provider_name(self, bs_view):
        # provicer_name
        bs_view_info = bs_view.find('div', class_='qQKdcc')
        provider_info = bs_view_info.findAll('span')[0].text
        return provider_info

    def provider_name_error(self, bs_view):
        # provicer_name
        bs_view_info = bs_view.find('div', class_='qQKdcc')
        provider = bs_view_info.findAll('span')[0].text
        provider_info = provider.encode('ascii', 'ignore').decode('utf-8')
        return provider_info

    # developer_id / dev_id 분리 .
    def developer_id(self, bs_view):
        # developer_name
        developer_view = bs_view.findAll('a', attrs={'class': 'hrTbp R8zArc'})
        developer_info = developer_view[0].get('href')

        developer_temp2 = str(developer_info)
        developer_temp = developer_temp2.split('=')
        if developer_temp[0]=='/store/apps/dev?id':
            dev_info = developer_temp[1]
            developer_info = ""
            return developer_info, dev_info
        else:
            developer_info = developer_temp[1]
            dev_info = ""
            return developer_info, dev_info

    def category_name(self, bs_view):
        # category_name
        bs_view_info = bs_view.find('div', class_='qQKdcc')
        category_info = bs_view_info.findAll('span')[1].text
        category_name = category_info
        return category_name

    def category_name_error(self, bs_view):
        # category_name
        bs_view_info = bs_view.find('div', class_='qQKdcc')
        category_info = bs_view_info.findAll('span')[1].text
        category_name = category_info.encode('ascii', 'ignore').decode('utf-8')
        return category_name

    def review_cnt(self, bs_view):
        # review_cnt
        try:
            review_elem = bs_view.find('div', class_='dNLKff')
            review_info = review_elem.findAll('span')[0].text
            review_temp1 = review_info.split(",")
            review_temp2 = "".join(review_temp1)
            review_cnt = float(review_temp2)
            return review_cnt
        except:
            review_cnt ='0'
            return review_cnt


    def down_update_elem(self, bs_view):
        # 업데이트 날짜와 다운로드 수
        try:
            down_elem = {}
            down_view = bs_view.findAll('span', class_='htlgb')
            d = 0
            for down in down_view:
                d = d + 1
                down_elem[d] = down.text
            # 첫번째 elem는 업데이트 날짜를 뜻함.
            update_name = down_elem[1]
            # 6번째 elem는 다운로드 수를 뜻하며, 10,000+ 형식이기 때문에 +와,문자를 제외한 후 text를 int로 변환시킴.
            down_temp1 = down_elem[6].split("+")[0]
            down_temp2 = down_temp1.split(",")
            down_temp3 = "".join(down_temp2)
            down_cnt = float(down_temp3)
            return update_name, down_cnt
        # 무료, 유료 카테고리 별 클래스 위치값이 달라지므로 조정해줌.
        except ValueError:
            update_name = down_elem[4]
            down_temp1 = down_elem[8].split("+")[0]
            down_temp2 = down_temp1.split(",")
            down_temp3 = "".join(down_temp2)
            down_cnt = float(down_temp3)
            return update_name, down_cnt

    def app_name_ascii(self, bs_view):
        App_name_elem = bs_view.find('h1', class_='AHFaub').text
        app_name = App_name_elem.encode('ascii', 'ignore').decode('utf-8')
        return app_name

    def app_name_euckr(self, bs_view):
        App_name_elem = bs_view.find('h1', class_='AHFaub').text
        app_name = App_name_elem.encode('euc-kr', 'ignore').decode('euc-kr')
        return app_name

    def app_name_ascii_error2(self, bs_view):
        App_name_elem = bs_view.find('h1', class_='AHFaub').text
        app_name = App_name_elem.encode("utf-8").decode('euc-kr')
        return app_name

    def site(self, bs_view):
        site_view = bs_view.findAll('a', attrs={'class': 'hrTbp'})
        site = site_view[3].get('href')
        return site

    def site_name(self, site):
        try:
            site_temp1 = site.split(':')
            try:
                site_temp2 = site_temp1[1][2:]
                site_temp3 = site_temp2.split('/')
                site_name = site_temp3[0]
                if site_temp1[0] == "mailto":
                    site_name = site.split(':')[1]
            except:
                site_name = site_temp1[1]
            return site_name
        except AttributeError:
            site_name = str(site)
            return site_name


