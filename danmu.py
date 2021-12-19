import re
import requests


def get_info(vid):
    url = f"https://api.bilibili.com/x/web-interface/view/detail?bvid={vid}"
    response = requests.get(url)
    response.encoding = "utf-8"
    data = response.json()
    info = {}
    info["标题"] = data["data"]["View"]["title"]
    info["总弹幕数"] = data["data"]["View"]["stat"]["danmaku"]
    info["视频数量"] = data["data"]["View"]["videos"]
    info["cid"] = [dic["cid"] for dic in data["data"]["View"]["pages"]]
    if info["视频数量"] > 1:
        info["子标题"] = [dic["part"] for dic in data["data"]["View"]["pages"]]
    for k, v in info.items():
        print(k + ":", v)
    return info


def get_danmu(info):
    all_dms = []
    for i, cid in enumerate(info["cid"]):
        url = f"https://api.bilibili.com/x/v1/dm/list.so?oid={cid}"
        response = requests.get(url)
        response.encoding = "utf-8"
        data = re.findall('<d p="(.*?)">(.*?)</d>', response.text)
        dms = [d[1] for d in data]
        if info["视频数量"] > 1:
            print("cid:", cid, "弹幕数:", len(dms), "子标题:", info["子标题"][i])
        all_dms += dms
    print(f"共获取弹幕{len(all_dms)}条！")
    return all_dms


if __name__ == "__main__":
    vid = input("请输入视频编号: ")
    info = get_info(vid)
    danmu = get_danmu(info)
    with open("danmu.txt", "w", encoding="utf-8") as fout:
        for dm in danmu:
            fout.write(dm + "\n")
