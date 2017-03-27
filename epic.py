# coding=utf-8
from __future__ import division, absolute_import, print_function, unicode_literals
import dateutil.parser
from dateutil.relativedelta import relativedelta
import requests
import requests.auth
import datetime


class EPIC(object):
    """ A programmatic interface to the processed DSCOVR EPIC imagery. """
    ENDPOINT = 'https://epic.gsfc.nasa.gov'
    EPOCH = datetime.datetime(2015, 6, 14)  # Date of first EPIC image

    def __init__(self, p_image_type=None, proxies=None):
        """
        initialize EPIC factory
        :param p_image_type: epic image collection : natural or enhanced
        :param proxies: proxy setup
        """
        self.session = requests.Session()
        self.session.trust_env = False
        if proxies is not None:
            self.session.proxies = proxies
        # if proxy_auth is not None:
        #     self.session.auth = requests.auth.HTTPProxyAuth(proxy_auth['login'],proxy_auth['password'])

        self.image_type = "{}".format(p_image_type)

    """
    Get most recent images
    """
    def get_most_recent_images(self):

        response = self.session.get(self.ENDPOINT + '/api/' + self.image_type, timeout=10)
        response.raise_for_status()
        # list_images = []
        for row in response.json():
            row['date'] = dateutil.parser.parse(row['date'])
            yield row
            # list_images.append(row)

        # return list_images

    """
    Get images for specific day
    """
    def get_images_for_date(self, date):

        response = self.session.get(self.ENDPOINT + '/api/' + self.image_type + '/date/' + date.isoformat(), timeout=10)
        response.raise_for_status()
        for row in response.json():
            row['date'] = dateutil.parser.parse(row['date'])
            yield row

    """
    Get recent image since the last x days
    """
    def get_recent_images(self, since, count=None, reverse=True):
        date = datetime.date.today()
        list_images = []
        finished = False
        while (count is None or len(list_images) < count) and not finished:
            for row in sorted(self.get_images_for_date(date), key=lambda image: image['date'], reverse=True):
                list_images.append(row)
                if row['date'] <= since or row['date'] <= self.EPOCH:
                    finished = True
                    break

            date -= relativedelta(days=1)
        list_images = sorted(list_images, key=lambda image: image['date'], reverse=reverse)
        if count is not None:
            list_images = list_images[:count]
        return list_images

    """
    Get images between 2 dates
    """
    def get_image_range(self, since, until):
        date = since
        images = []
        while date <= until:
            images.extend(self.get_images_for_date(date))
            date += relativedelta(days=1)
        return sorted(images, key=lambda image: image['date'])

    """
    Download a specific image by name
    """
    def download_image(self, metadata, fp):

        url = "%s/archive/%s/%s/%s/%s/jpg/%s.jpg" % (self.ENDPOINT,
                                                        self.image_type,
                                                        metadata['date'].strftime('%Y'),
                                                        metadata['date'].strftime('%m'),
                                                        metadata['date'].strftime('%d'),
                                                        metadata['image'],
                                                        )
        response = self.session.get(url, stream=True, timeout=30)
        response.raise_for_status()
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                fp.write(chunk)
        fp.flush()
