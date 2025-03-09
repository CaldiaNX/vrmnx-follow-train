__title__ = "ついてくん Ver.1.0"
__author__ = "Caldia"
__update__  = "2025/03/10"

import vrmapi

# ファイル読み込みの確認用
vrmapi.LOG("import " + __title__)

# 初期化時にmin-Maxを定義するコンストラクタ
def vrmevent_init(obj,ev,param, min, max):
    if ev == 'init':
        # 初期化
        di = obj.GetDict()
        di['ft_search_min'] = min
        di['ft_search_max'] = max
        di['ft_search_ato'] = 0
        # フレームイベント登録
        obj.SetEventFrame()
    else:
        # 他イベントはmain
        vrmevent(obj,ev,param)

# main
def vrmevent(obj,ev,param):
    if ev == 'init':
        # 初期化
        di = obj.GetDict()
        di['ft_search_min'] = 60.0
        di['ft_search_max'] = 100.0
        di['ft_search_ato'] = 0
        # フレームイベント登録
        obj.SetEventFrame()
    elif ev == 'frame':
        di = obj.GetDict()
        # 最大探知距離に居ない
        searchId = obj.SearchForwardTrainID(di['ft_search_max'])
        if searchId == 0:
            # 車内信号が進行以外
            if di['ft_search_ato'] != 6:
                # 最大速度
                obj.AutoSpeedCTRL(di['ft_search_min'], 1.0)
                di['ft_search_ato'] = 6
                # 確認用ログ
                #vrmapi.LOG("{0} [{1}] 進行 ({2}-{3})".format(obj.GetNAME(), obj.GetID(), di['ft_search_min'], di['ft_search_max']))
        # 最小探知以下に居る
        elif obj.SearchForwardTrainID(di['ft_search_min']) != 0:
            # 車内信号が停止以外
            if di['ft_search_ato'] != 0:
                # 停止
                obj.AutoSpeedCTRL(di['ft_search_min'] / 2, 0.0)
                di['ft_search_ato'] = 0
                # 確認用ログ
                #vrmapi.LOG("{0} [{1}] 停止 ({2}-{3})".format(obj.GetNAME(), obj.GetID(), di['ft_search_min'], di['ft_search_max']))
        # 最大探知距離と最小探知距離の間に居る
        else:
            # 車内信号が注意以外
            if di['ft_search_ato'] != 3:
                # 注意速度
                ftr = vrmapi.LAYOUT().GetTrain(searchId)
                obj.AutoSpeedCTRL(di['ft_search_min'], ftr.GetVoltage() * 0.9)
                di['ft_search_ato'] = 3
                # 確認用ログ
                #vrmapi.LOG("{0} [{1}] 注意 ({2}-{3})".format(obj.GetNAME(), obj.GetID(), di['ft_search_min'], di['ft_search_max']))
