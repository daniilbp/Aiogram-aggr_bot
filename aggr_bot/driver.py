import json
from datetime import datetime, timedelta
import asyncio
from random import random

from additions.addition import msg_error, groups_type, inp_exm, ans_exm
from tools.pymongo_clients import connect_atlas
from tools.utils import delta_calc_month, delta_calc_day, delta_calc_hour, sync_vers


client = connect_atlas()
coll = client.sampleDB.sample_collection

delta_methods = {"month": delta_calc_month, "day": delta_calc_day, "hour": delta_calc_hour,}


async def msg_is_valid(msg: str) -> dict[str, datetime | str]:
    """Функция проверки валидности запроса"""
    valid_data = {}
    try:
        req = json.loads(msg)
        assert 'dt_from' in req and 'dt_upto' in req and 'group_type' in req and len(req) == 3, msg_error[0]

        valid_data["dt_from"] = datetime.fromisoformat(req['dt_from'])
        valid_data["dt_upto"] = datetime.fromisoformat(req['dt_upto'])
        valid_data["group_type"] = groups_type[req['group_type']]
    except AssertionError as exc:
        valid_data["error"] = exc
    except Exception as exc:
        valid_data["error"] = msg_error[1]

    return valid_data


async def get_agg_data(dt_from: datetime, dt_to: datetime, i: int, res_before_sort: dict):
    """функция-задача агрегирующая данные за период"""
    docs: list = coll.find({"dt": {"$gte": dt_from, "$lt": dt_to}})
    res: int = sum([doc['value'] for doc in docs])
    res_before_sort[i] = [res, dt_from]
    
    await asyncio.sleep(random()) #блокировка на некоторое время для проверки асинхронности
    print(f">>>task {i} done<<<")


async def get_all_agg_data(msg: str) -> str:
    """
    Функция генерирующая очередь асинхронных задач,
    если запрос прошел валидацию.
    Где кол-во задач определяется циклом while с шагом (интервалом),
    который определяется ч/з вспомогательные ф-иии исходя из запроса.
    """
    print(f">Start get_all_agg_data at {(st := datetime.now())}<")

    params: dict = await msg_is_valid(msg)
   
    if not params.get('error'):
        print(f">>params is valid<<")
        
        delta_method: function = delta_methods[params["group_type"]]
        tasks, i, res_before_sort = [], 0, {}

        while params["dt_from"] <= params["dt_upto"]:
            delta: timedelta = await delta_method(params["dt_from"])
            dt_temp: datetime = params["dt_from"] + delta
            if dt_temp > params["dt_upto"]: dt_temp = params["dt_upto"] + timedelta(seconds=1)
            
            tasks.append(get_agg_data(params["dt_from"], dt_temp, i, res_before_sort))
            
            params["dt_from"] = dt_temp
            i += 1
        
        await asyncio.gather(*tasks) #выполнение задач
        
        ans = {"dataset": [], "labels": []}
        for el in sorted(res_before_sort.items()):
            ans["dataset"].append(el[1][0])
            ans["labels"].append(el[1][1].isoformat(sep='T', timespec='auto'))
        
        print(f">Done get_all_agg_data at {datetime.now() - st}<")

        return json.dumps(ans)
    else:
        print(f"{params["error"]}")
        return params["error"]


def main(msg: str) -> str:
    """Функция запускающая асинхронное выполнение задач при запросе"""
    ans = asyncio.run(get_all_agg_data(msg))
    return ans


if __name__ == "__main__":
    stt = datetime.now()
    for interval in range(3):
        ans = main(inp_exm[interval])
        print(ans == json.dumps(ans_exm[interval]))

        ans = sync_vers(inp_exm[interval], coll)
        print(ans == json.dumps(ans_exm[interval]))
    print(f"Tot time is {datetime.now() - stt}")