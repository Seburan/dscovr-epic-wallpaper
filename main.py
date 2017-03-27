# coding: utf-8
# Created on 2017/03/16
# @author: Severin Ferrand

# based on https://epic.gsfc.nasa.gov/about/api version 2.0

# The code is tested to be working on:
# Windows-7-6.1.7601-SP1
# Python Version: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)] on win32

import epic
import datetime
import logging
import os
import errno
import ctypes
import argparse

from requests import ConnectionError

# Constant for Windows Desktop Wallpaper setup
#SPI_SETDESKWALLPAPER = 0x0014   # working
#SPI_SETDESKWALLPAPER = 0x14     # working
SPI_SETDESKWALLPAPER = 20        # working
# SPIF_UPDATEINIFILE   = 0x2      #forces instant update

g_debug = False

def init_directory(directory_path):
    """
    Create a directory if not exists
    :param directory_path: relative path
    :return:
    """

    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    return 0


def init_image_directory(p_work_path):
    """
    initialize the image directory
    :return:
    """
    image_path = os.path.normpath(p_work_path + "/images/")

    init_directory(image_path)

    return image_path


def init_log(p_work_path):
    """
    initialize the log directory
    :return:
    """
    log_path = os.path.normpath(p_work_path + "/logs/")

    init_directory(log_path)

    log_file_path =  os.path.normpath(log_path + "/epic.log")

    logging.basicConfig(filename=log_file_path,
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s')

    return log_file_path


def update_wallpaper(wallpaper_image_file_path):
    global g_debug

    """
    Update Wallpaper (Works with Windows 7 x64)
    wallpaper_image_file_path : absolute path]

    See :
    https://www.blog.pythonlibrary.org/2014/10/22/pywin32-how-to-set-desktop-background/
    http://code.activestate.com/recipes/435877-change-the-wallpaper-under-windows/

    :param wallpaper_image_file_path: absolute path to JPEG image
    :return: return code from windows
    """

    rc = ctypes.windll.user32.SystemParametersInfoA(
        SPI_SETDESKWALLPAPER,
        0,
        ctypes.create_string_buffer(wallpaper_image_file_path),
        0)
    if g_debug:
        print ("Set Wallpaper Return Code : {}".format(rc))

    return rc


def main():
    """
    Main Process
    """
    global g_debug

    p_collection = None
    p_date = None
    p_position = None
    p_wallpaper = False
    p_proxies = None

    # return code
    return_code = 0

    # set workpath in user's home
    work_path = os.path.expanduser("~")
    work_path = os.path.normpath(work_path + "/.dscovr-epic-wallpaper/")

    # initialize log
    init_log(work_path)

    # setup argument parser
    parser = argparse.ArgumentParser(description='Toolbox for epic.gsfc.nasa.gov API')

    # args : debug
    parser.add_argument("--debug", help="Enable verbose logging", action="store_true")

    # args: collection
    # Use collection of images
    # natural
    # enhanced
    parser.add_argument("--collection",
                        choices=[
                            "natural",
                            "enhanced",
                        ],
                        default="natural",
                        help="Select collection of images. 'natural' or 'enhanced' "
                             "Default : if not specified, lookup form natural image collection")

    # args : date
    # date of picture
    parser.add_argument("--date",
                        help="[Optional] Date of the picture "
                             "Default : if not specified, this is the latest day available")

    position_group = parser.add_mutually_exclusive_group()
    # args : position
    # Earth Position in Universal Time
    # 00:00:00 is aligned with International Date Line (east)
    # 12:00:00 is aligned with London
    # 00:00:00 is aligned with International Date Line (west)
    position_group.add_argument("--position", type=int,
                        choices=range(24),
                        help="[Optional] Earth position (in Universal Time 0-23)) "
                             "Default : if not specified, lookup the latest position")

    # args : now
    # reflect position as current hour
    position_group.add_argument("--now",
                        help="[Optional] Reflect earth position as current hour",
                        action="store_true")


    # args : wallpaper
    parser.add_argument("--wallpaper",
                        help="[Optional] Update Windows Desktop Wallpaper",
                        action="store_true")

    # args : proxy-host
    parser.add_argument("--proxy-host",
                        help="[Optional] Proxy host:port")

    # args : group-proxy
    group_proxy_auth = parser.add_argument_group()
    # proxy-login
    group_proxy_auth.add_argument("--proxy-login",
                        help="[Optional] Proxy Login")

    # args : proxy-password
    group_proxy_auth.add_argument("--proxy-password",
                        help="[Optional] Proxy Password")

    # finally parse arguments
    args = parser.parse_args()

    # enable debug
    if args.debug:
        g_debug = True

    # select collection of images
    if args.collection:
        if args.collection == 'enhanced':
            p_collection = "enhanced"
        elif args.collection == 'natural':
            p_collection = "natural"

    # select date : default format is dd/MM/yy
    if args.date:
        # parse date
        try:
            p_date = datetime.datetime.strptime(args.date, "%x").date()

        except ValueError:
            logging.exception("invalid date format")
            print 'Exception raised : "{} is not a valid date". See logs for details.'.format(args.date)
            return_code = 1
            # exit(1)

    # select earth position
    if args.position:
        if 0 <= args.position <= 23:
            p_position = int(args.position)
    elif args.now:
        p_position = datetime.datetime.utcnow().hour

    # change wallpaper ?
    if args.wallpaper:
        p_wallpaper = True

    # setup proxies
    if args.proxy_host:

        if args.proxy_login and args.proxy_password:

            p_proxies = {
                'http': 'http://{}:{}@{}'.format(args.proxy_login,
                                                                                 args.proxy_password,
                                                                                 args.proxy_host),
                'https': 'https://{}:{}@{}'.format(args.proxy_login,
                                                                                 args.proxy_password,
                                                                                 args.proxy_host),
            }
        else:
            p_proxies = {
                'http': 'http://{}'.format(args.proxy_host),
                'https': 'https://{}'.format(args.proxy_host),
            }

    # Main Process Start
    if g_debug:
        print("Main : Start")

    # initialize image directory
    image_path = init_image_directory(work_path)

    # EPIC facility
    epic_factory = epic.EPIC(p_image_type=p_collection, proxies=p_proxies)

    try:
        if g_debug:
            print "Looking for image metadata. Date = {} Position = {}".format(p_date, p_position)

        # lookup list of images for date
        if p_date is None :
            # fetch the images metadata from latest available day
            target_day_images = epic_factory.get_most_recent_images()
        else :
            # fetch the image  metadata from specific date
            target_day_images = epic_factory.get_images_for_date(p_date)

        # lookup target image for position
        target_image = None
        if p_position is None :
            # if no position specified, get the latest available
            for target_image in target_day_images:
                pass
        else :
            # if specified, try to find the nearest position

            previous_delta = None
            for image in target_day_images:
                nearest_date = image['date'].replace(hour=p_position, minute=0, second=0, microsecond=0)
                delta = nearest_date - image['date']
                delta = abs(delta.total_seconds())
                if previous_delta is not None:
                    if delta > previous_delta :
                        break
                previous_delta = delta
                target_image = image

        # if we could not find an image, raise error
        if target_image is None:
            logging.error("No target image available for parameters Date = {} Position = {}".format(p_date, p_position))
            print "No target image available for parameters Date = {} Position = {}".format(p_date, p_position)
            exit(2)

        if g_debug:
            print "Target image is : {}".format(target_image)

        # fetch the target image itself
        latest_image_file_path = os.path.normpath(image_path + "/" + target_image['image'] + '.jpg')
        with open(latest_image_file_path, mode="wb") as latest_image_file:
            epic_factory.download_image(target_image, latest_image_file)

        # update screensaver
        if p_wallpaper:
            wallpaper_image_file_absolute_path = os.path.abspath(latest_image_file_path)
            update_wallpaper(wallpaper_image_file_absolute_path)

    except (ConnectionError, ValueError):
        logging.exception("Unable to fetch images")
        print 'Exception raised : "Unable to fetch images". See logs for details.'
        return_code = 2
        # exit(2)
    except IndexError:
        logging.exception("No images available")
        print 'Exception raised : "No images available". See logs for details.'
        return_code = 3
        # exit(3)

    if g_debug:
        print("Main : End")

    return return_code

if __name__ == '__main__':
    # main function
    main_return_code = main()
    exit(main_return_code)

