import calendar
from datetime import datetime, timedelta
import json
from random import random
from time import sleep

from additions.addition import msg_error, groups_type


async def delta_calc_month(dt_from: datetime) -> timedelta:
    """
    Техническая функция для рассчета дэльты (шага) до нового месяца.
    
    Args:
        dt_from (datetime): дата от (левая граница диапазона дат) которой нужно рассчитать дэльту
    Returns:
        (timedelta): дэльта до нового месяца
    """
    dim = calendar.monthrange(dt_from.year, dt_from.month)[1] # days in month (dim)
    return timedelta(days=(dim-dt_from.day), hours=(23-dt_from.hour),
                        minutes=(59-dt_from.minute), seconds=(60-dt_from.second))


async def delta_calc_day(dt: datetime) -> timedelta:
    """
    Техническая функция для рассчета дэльты (шага) до нового дня.
    
    Args:
        dt_from (datetime): дата от (левая граница диапазона дат) которой нужно рассчитать дэльту
    Returns:
        (timedelta): дэльта до нового дня
    """
    return timedelta(hours=(23-dt.hour), minutes=(59-dt.minute), seconds=(60-dt.second))


async def delta_calc_hour(dt: datetime) -> timedelta:
    """
    Техническая функция для рассчета дэльты (шага) до нового часа.
    
    Args:
        dt_from (datetime): дата от (левая граница диапазона дат) которой нужно рассчитать дэльту
    Returns:
        (timedelta): дэльта до нового часа
    """
    return timedelta(minutes=(59-dt.minute), seconds=(60-dt.second))


def delta_calc_month_sync(dt_from: datetime) -> timedelta:
    dim = calendar.monthrange(dt_from.year, dt_from.month)[1] # days in month (dim)
    return timedelta(days=(dim-dt_from.day), hours=(23-dt_from.hour),
                        minutes=(59-dt_from.minute), seconds=(60-dt_from.second))


def delta_calc_day_sync(dt: datetime) -> timedelta:
    return timedelta(hours=(23-dt.hour), minutes=(59-dt.minute), seconds=(60-dt.second))


def delta_calc_hour_sync(dt: datetime) -> timedelta:
    return timedelta(minutes=(59-dt.minute), seconds=(60-dt.second))


delta_methods_sync = {"month": delta_calc_month_sync, "day": delta_calc_day_sync, "hour": delta_calc_hour_sync,}


def sync_vers(msg, coll=None):
    if coll is None:
        from tools.pymongo_clients import connect_atlas

        client = connect_atlas()
        coll = client.sampleDB.sample_collection

    print(f">SYNC Start get_all_agg_data at {(st := datetime.now())}<")
    
    ans = {"dataset": [], "labels": []}
    valid_data = {}
    try:
        req = json.loads(msg)
        assert 'dt_from' in req and 'dt_upto' in req and 'group_type' in req and len(req) == 3, msg_error[0]

        valid_data["dt_from"] = datetime.fromisoformat(req['dt_from'])
        valid_data["dt_upto"] = datetime.fromisoformat(req['dt_upto'])
        valid_data["group_type"] = groups_type[req['group_type']]
    except AssertionError as exc:
        print("AssertionError")
        valid_data["error"] = exc
    except Exception as exc:
        print(f"Exception: {exc}")
        valid_data["error"] = msg_error[1]
    print(f">>>params is valid<<<")
    
    if not valid_data.get('error'):
        delta_method: function = delta_methods_sync[valid_data["group_type"]]
        i = 0
        while valid_data["dt_from"] <= valid_data["dt_upto"]:
            delta: timedelta = delta_method(valid_data["dt_from"])
            dt_temp: datetime = valid_data["dt_from"] + delta
            if dt_temp > valid_data["dt_upto"]: dt_temp = valid_data["dt_upto"] + timedelta(seconds=1)

            docs: list = coll.find({"dt": {"$gte": valid_data["dt_from"], "$lt": dt_temp}})
            res: int = sum([doc['value'] for doc in docs])

            # блокировка на некоторое время
            sleep(random())
            print(f"task {i} done")

            ans["labels"].append(valid_data["dt_from"].isoformat(sep='T', timespec='auto'))
            ans["dataset"].append(res)
            
            valid_data["dt_from"] = dt_temp
            i += 1
      
    else:
        print(f"{valid_data["error"]}")
        ans["error"] = valid_data["error"]

    print(f">SYNC Done get_all_agg_data at {datetime.now() - st}<")
    
    return json.dumps(ans)
