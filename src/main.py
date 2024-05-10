import xml.etree.ElementTree as ET
import pandas as pd
from typing import Tuple
import os

def getChildren(df:pd.DataFrame, node:any,area:str,id:str,lod:int) -> Tuple[pd.DataFrame,str]:
    if len(node) > 0:
        for child in node:
            # 建物IDの取得
            # child.attrib オブジェクトが "id" キーを持っているか確認
            if id == "" and "{http://www.opengis.net/gml}id" in child.attrib:
                id = child.attrib["{http://www.opengis.net/gml}id"]
                print("id is:"+id)
            else:
                print("id is not in child.attrib")

            # lodの取得
            if "{http://www.opengis.net/citygml/building/2.0}lod0FootPrint" in child.tag:
                lod = 0
            elif "{http://www.opengis.net/citygml/building/2.0}lod1Solid" in child.tag:
                lod = 1
            elif "{http://www.opengis.net/citygml/building/2.0}lod2Solid" in child.tag:
                lod = 2
            else:
                lod = lod

            df,id = getChildren(df,child,area,id,lod)
            if child.tag == "{http://www.opengis.net/gml}posList":
                # textの中身の数を調べる
                positionNum = int(child.text.count(" ")/3)
                print(positionNum)
                for i in range(int(positionNum)):
                    new_row = {'area':area,'id':id,'lod':lod, 'lat':child.text.split(" ")[i*3], 'lon':child.text.split(" ")[i*3 + 1], 'height':child.text.split(" ")[i*3 +2]}
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    print(new_row)
    return df,id

file = "52364657_bldg_6697_op.gml"
area = file.split(".")[0]
tree = ET.parse('../input/52364657_bldg_6697_op.gml')
roots = tree.getroot()
rootNum = len(roots)
for value in range(rootNum):
    if value <2:
        continue
    cityObjectMember = roots[value]
    df = pd.DataFrame(columns=['area','id', 'lod', 'lat', 'lon', 'height'])
    df,id = getChildren(df,cityObjectMember, area,id="",lod=0)

    # area ディレクトリがない場合は作成
    if not os.path.exists(f"../output/{area}"):
        os.makedirs(f"../output/{area}/building/")
    df.to_csv(f"../output/{area}/building/{id}.csv", index=False)
    print(f"../output/{area}/building/{id}.csv")
