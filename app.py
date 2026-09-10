import streamlit as st
import pandas as pd

# 1. 页面基本设置
st.set_page_config(page_title="投资信息本地看板", layout="wide")
st.title("📊 每日融资投资信息看板 (本地版)")

# 2. 核心引擎：地址标准化与三级拆解
@st.cache_data
def load_data(file_path):
    df = pd.read_excel(file_path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    if '日期' in df.columns:
        df['日期'] = pd.to_datetime(df['日期'], errors='coerce')
        df = df.sort_values(by='日期', ascending=False)
    
    def parse_address(loc):
        if pd.isna(loc) or str(loc).strip().lower() == 'nan':
            return '未知', '未知', '未知'
        
        loc = str(loc).strip().replace('-', '')
        
        district_map = {
            '海淀': ('北京市', '北京市', '海淀区'), '海淀区': ('北京市', '北京市', '海淀区'),
            '东城': ('北京市', '北京市', '东城区'), '东城区': ('北京市', '北京市', '东城区'),
            '大兴': ('北京市', '北京市', '大兴区'), '大兴区': ('北京市', '北京市', '大兴区'),
            '昌平': ('北京市', '北京市', '昌平区'), '昌平区': ('北京市', '北京市', '昌平区'),
            '西城': ('北京市', '北京市', '西城区'), '西城区': ('北京市', '北京市', '西城区'),
            '怀柔': ('北京市', '北京市', '怀柔区'), '怀柔区': ('北京市', '北京市', '怀柔区'),
            '朝阳': ('北京市', '北京市', '朝阳区'), '朝阳区': ('北京市', '北京市', '朝阳区'),
            '通州': ('北京市', '北京市', '通州区'), '通州区': ('北京市', '北京市', '通州区'),
            '石景山': ('北京市', '北京市', '石景山区'), '石景山区': ('北京市', '北京市', '石景山区'),
            
            '黄浦': ('上海市', '上海市', '黄浦区'), '黄浦区': ('上海市', '上海市', '黄浦区'),
            '闵行': ('上海市', '上海市', '闵行区'), '闵行区': ('上海市', '上海市', '闵行区'),
            '嘉定': ('上海市', '上海市', '嘉定区'), '嘉定区': ('上海市', '上海市', '嘉定区'),
            '浦东新区': ('上海市', '上海市', '浦东新区'),
            '奉贤': ('上海市', '上海市', '奉贤区'), '奉贤区': ('上海市', '上海市', '奉贤区'),
            '普陀': ('上海市', '上海市', '普陀区'), '普陀区': ('上海市', '上海市', '普陀区'),
            '金山': ('上海市', '上海市', '金山区'), '金山区': ('上海市', '上海市', '金山区'),
            '青浦': ('上海市', '上海市', '青浦区'), '青浦区': ('上海市', '上海市', '青浦区'),
            '宝山': ('上海市', '上海市', '宝山区'), '宝山区': ('上海市', '上海市', '宝山区'),
            '杨浦': ('上海市', '上海市', '杨浦区'), '杨浦区': ('上海市', '上海市', '杨浦区'),
            '松江': ('上海市', '上海市', '松江区'), '松江区': ('上海市', '上海市', '松江区'),
            '徐汇': ('上海市', '上海市', '徐汇区'), '徐汇区': ('上海市', '上海市', '徐汇区'),
            '长宁': ('上海市', '上海市', '长宁区'), '长宁区': ('上海市', '上海市', '长宁区'),
            '静安': ('上海市', '上海市', '静安区'), '静安区': ('上海市', '上海市', '静安区'),
            '虹口': ('上海市', '上海市', '虹口区'), '虹口区': ('上海市', '上海市', '虹口区'),
            
            '渝北': ('重庆市', '重庆市', '渝北区'), '渝北区': ('重庆市', '重庆市', '渝北区'),
            '巴南': ('重庆市', '重庆市', '巴南区'), '巴南区': ('重庆市', '重庆市', '巴南区'),
            '江北': ('重庆市', '重庆市', '江北区'), '江北区': ('重庆市', '重庆市', '江北区'),
            '北碚': ('重庆市', '重庆市', '北碚区'), '北碚区': ('重庆市', '重庆市', '北碚区'),
            '涪陵': ('重庆市', '重庆市', '涪陵区'), '涪陵区': ('重庆市', '重庆市', '涪陵区'),
            '南岸': ('重庆市', '重庆市', '南岸区'), '南岸区': ('重庆市', '重庆市', '南岸区'),
            '西青': ('天津市', '天津市', '西青区'), '西青区': ('天津市', '天津市', '西青区'),
            '津南': ('天津市', '天津市', '津南区'), '津南区': ('天津市', '天津市', '津南区'),
            '滨海新区': ('天津市', '天津市', '滨海新区'), 
            
            '广州市番禺区': ('广东省', '广州市', '番禺区'), '深圳市南山区': ('广东省', '深圳市', '南山区'),
            '深圳市龙华区': ('广东省', '深圳市', '龙华区'), '深圳市福田区': ('广东省', '深圳市', '福田区'),
            '南京市江北新区': ('江苏省', '南京市', '江北新区'), '苏州高新区': ('江苏省', '苏州市', '高新区'),
            '合肥高新区': ('安徽省', '合肥市', '高新区'), '成都高新区': ('四川省', '成都市', '高新区'),
            '合肥蜀山区': ('安徽省', '合肥市', '蜀山区'), '长沙湘江新区': ('湖南省', '长沙市', '湘江新区'),
            '苏州吴江': ('江苏省', '苏州市', '吴江区'), '苏州吴中': ('江苏省', '苏州市', '吴中区'),
            '东莞滨海湾': ('广东省', '东莞市', '滨海湾新区'), '无锡梁溪': ('江苏省', '无锡市', '梁溪区'),
            '苏州昆山': ('江苏省', '苏州市', '昆山市'), '长沙高新开发区': ('湖南省', '长沙市', '高新开发区'),
            '香港九龙城区': ('香港特别行政区', '香港特别行政区', '九龙城区'), '香港屯门区': ('香港特别行政区', '香港特别行政区', '屯门区')
        }
        
        city_map = {
            '深圳': ('广东省', '深圳市'), '广州': ('广东省', '广州市'), '东莞': ('广东省', '东莞市'), 
            '佛山': ('广东省', '佛山市'), '珠海': ('广东省', '珠海市'), '中山': ('广东省', '中山市'), '江门': ('广东省', '江门市'),
            '常州': ('江苏省', '常州市'), '苏州': ('江苏省', '苏州市'), '南京': ('江苏省', '南京市'), 
            '无锡': ('江苏省', '无锡市'), '南通': ('江苏省', '南通市'), '扬州': ('江苏省', '扬州市'), 
            '镇江': ('江苏省', '镇江市'), '淮安': ('江苏省', '淮安市'), '宿迁': ('江苏省', '宿迁市'), 
            '盐城': ('江苏省', '盐城市'), '常熟': ('江苏省', '苏州市'), 
            '宁波': ('浙江省', '宁波市'), '嘉兴': ('浙江省', '嘉兴市'), '杭州': ('浙江省', '杭州市'), 
            '绍兴': ('浙江省', '绍兴市'), '湖州': ('浙江省', '湖州市'), '衢州': ('浙江省', '衢州市'), 
            '金华': ('浙江省', '金华市'), '丽水': ('浙江省', '丽水市'),
            '淄博': ('山东省', '淄博市'), '济南': ('山东省', '济南市'), '泰安': ('山东省', '泰安市'), 
            '威海': ('山东省', '威海市'), '青岛': ('山东省', '青岛市'), '东营': ('山东省', '东营市'), 
            '济宁': ('山东省', '济宁市'), '滨州': ('山东省', '滨州市'), '潍坊': ('山东省', '潍坊市'), 
            '菏泽': ('山东省', '菏泽市'), '烟台': ('山东省', '烟台市'),
            '长沙': ('湖南省', '长沙市'), '益阳': ('湖南省', '益阳市'), '株洲': ('湖南省', '株洲市'), 
            '永州': ('湖南省', '永州市'), '常德': ('湖南省', '常德市'),
            '成都': ('四川省', '成都市'), '泸州': ('四川省', '泸州市'), '绵阳': ('四川省', '绵阳市'), 
            '德阳': ('四川省', '德阳市'), '遂宁': ('四川省', '遂宁市'), '乐山': ('四川省', '乐山市'), 
            '眉山': ('四川省', '眉山市'), '自贡': ('四川省', '自贡市'),
            '马鞍山': ('安徽省', '马鞍山市'), '合肥': ('安徽省', '合肥市'), '阜阳': ('安徽省', '阜阳市'), 
            '安庆': ('安徽省', '安庆市'), '淮南': ('安徽省', '淮南市'), '滁州': ('安徽省', '滁州市'), '芜湖': ('安徽省', '芜湖市'),
            '泉州': ('福建省', '泉州市'), '厦门': ('福建省', '厦门市'), '南平': ('福建省', '南平市'), 
            '漳州': ('福建省', '漳州市'), '福州': ('福建省', '福州市'), '莆田': ('福建省', '莆田市'),
            '赣州': ('江西省', '赣州市'), '九江': ('江西省', '九江市'), '抚州': ('江西省', '抚州市'), 
            '萍乡': ('江西省', '萍乡市'), '南昌': ('江西省', '南昌市'), '景德镇': ('江西省', '景德镇市'),
            '安阳': ('河南省', '安阳市'), '三门峡': ('河南省', '三门峡市'), '郑州': ('河南省', '郑州市'),
            '西安': ('陕西省', '西安市'), '铜川': ('陕西省', '铜川市'),
            '沈阳': ('辽宁省', '沈阳市'), '大连': ('辽宁省', '大连市'),
            '唐山': ('河北省', '唐山市'), '石家庄': ('河北省', '石家庄市'), '邯郸': ('河北省', '邯郸市'), 
            '张家口': ('河北省', '张家口市'), '承德': ('河北省', '承德市'),
            '长治': ('山西省', '长治市'), '临汾': ('山西省', '临汾市'),
            '大理': ('云南省', '大理市'), '昆明': ('云南省', '昆明市'),
            '儋州': ('海南省', '儋州市'), '海口': ('海南省', '海口市'),
            '武汉': ('湖北省', '武汉市'), '哈尔滨': ('黑龙江省', '哈尔滨市'), '张掖': ('甘肃省', '张掖市'), 
            '银川': ('宁夏回族自治区', '银川市'), '南宁': ('广西壮族自治区', '南宁市')
        }
        
        for k, v in district_map.items():
            if k in loc: return v[0], v[1], v[2]
                
        for k, v in city_map.items():
            if k in loc:
                dist_part = loc.replace(k, '').replace(v[0], '').replace('市', '').replace(v[0].replace('省',''), '')
                if dist_part:
                    if not dist_part.endswith(('区', '县', '市')): dist_part += '区'
                    return v[0], v[1], dist_part
                return v[0], v[1], "全部"

        municipalities = ['北京', '上海', '天津', '重庆']
        for m in municipalities:
            if loc.startswith(m):
                prov, city = m + '市', m + '市'
                dist_part = loc.replace(m, '').replace('市', '')
                if dist_part:
                    if not dist_part.endswith(('区', '县', '新区')): dist_part += '区'
                    return prov, city, dist_part
                return prov, city, "全部"
                
        provinces = ['广东', '江苏', '浙江', '山东', '四川', '安徽', '湖北', '湖南', '福建', '江西', '河南', '河北', '陕西', '山西', '辽宁', '吉林', '黑龙江', '云南', '贵州', '甘肃', '青海', '海南']
        for p in provinces:
            if loc.startswith(p):
                prov = p + '省'
                rem = loc.replace(p, '').replace('省', '')
                if rem:
                    if '市' in rem:
                        parts = rem.split('市')
                        city = parts[0] + '市'
                        dist = parts[1] + ('区' if parts[1] and not parts[1].endswith(('区','县')) else '')
                        return prov, city, dist if dist else "全部"
                    else:
                        city = rem + ('市' if not rem.endswith(('市','州','区','县')) else '')
                        return prov, city, "全部"
                return prov, "全部", "全部"

        return '其他', '其他', loc

    if '公司注册地' in df.columns:
        parsed = df['公司注册地'].apply(parse_address)
        df['省份'] = [x[0] for x in parsed]
        df['城市'] = [x[1] for x in parsed]
        df['区县'] = [x[2] for x in parsed]
    
    # 将缺失值填充为未知
    df = df.fillna("未知")
    return df

file_path = "每日融资信息.xlsx"
try:
    df = load_data(file_path)
    df = df.dropna(subset=['公司'])
except Exception as e:
    st.error(f"读取文件失败，请检查文件路径。错误信息：{e}")
    st.stop()

# 3. 侧边栏：三级联动检索体系 + 子行业联动
st.sidebar.header("🔍 数据检索与筛选")
search_query = st.sidebar.text_input("全局搜索 (公司名称/简介等)", "")

st.sidebar.markdown("---")
st.sidebar.markdown("**📍 地址三级联动筛选**")

provinces = ["全国"] + sorted([p for p in df['省份'].unique() if p not in ["未知", "其他"]])
selected_prov = st.sidebar.selectbox("1. 选择省/直辖市", provinces)

if selected_prov != "全国":
    city_options = df[df['省份'] == selected_prov]['城市'].unique().tolist()
    city_options = ["全市"] + sorted([c for c in city_options if c != "全部"])
else:
    city_options = ["请先选择省份"]
selected_city = st.sidebar.selectbox("2. 选择地级市", city_options, disabled=(selected_prov == "全国"))

if selected_city not in ["全市", "请先选择省份"]:
    dist_options = df[(df['省份'] == selected_prov) & (df['城市'] == selected_city)]['区县'].unique().tolist()
    dist_options = ["全区/县"] + sorted([d for d in dist_options if d != "全部" and d != "未知"])
else:
    dist_options = ["请先选择城市"]
selected_dist = st.sidebar.selectbox("3. 选择详细区县", dist_options, disabled=(selected_city in ["全市", "请先选择省份"]))

st.sidebar.markdown("---")
st.sidebar.markdown("**🏢 行业细分筛选**")

# ================= 新增：行业与子行业联动筛选 =================
industries = ["全部"] + sorted([str(x) for x in df['行业'].unique() if x != "未知"])
selected_ind = st.sidebar.selectbox("1. 按一级行业筛选", industries)

if selected_ind != "全部":
    sub_industries = df[df['行业'] == selected_ind]['子行业'].unique().tolist()
    sub_industries = ["全部"] + sorted([str(x) for x in sub_industries if x != "未知"])
else:
    sub_industries = ["全部"] + sorted([str(x) for x in df['子行业'].unique() if x != "未知"])
selected_sub_ind = st.sidebar.selectbox("2. 按子行业筛选 (细分赛道)", sub_industries)
# ==========================================================

# 4. 执行过滤逻辑
filtered_df = df.copy()

if search_query:
    mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
    filtered_df = filtered_df[mask]

if selected_prov != "全国":
    filtered_df = filtered_df[filtered_df['省份'] == selected_prov]
if selected_city not in ["全市", "请先选择省份"]:
    filtered_df = filtered_df[filtered_df['城市'] == selected_city]
if selected_dist not in ["全区/县", "请先选择城市"]:
    filtered_df = filtered_df[filtered_df['区县'] == selected_dist]

if selected_ind != "全部":
    filtered_df = filtered_df[filtered_df['行业'] == selected_ind]
if selected_sub_ind != "全部":
    filtered_df = filtered_df[filtered_df['子行业'] == selected_sub_ind]


# 5. 顶部数据指标卡片 (改为聚焦子行业)
st.markdown("### 📈 核心数据概览")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="当前筛选企业数", value=f"{len(filtered_df)} 家")
with col2:
    # 过滤掉“未知”再计算最热门子行业，避免出现“最热门行业是未知”的尴尬情况
    valid_sub_ind = filtered_df[filtered_df['子行业'] != '未知']['子行业']
    top_sub_ind = valid_sub_ind.value_counts().index[0] if len(valid_sub_ind) > 0 else "无"
    st.metric(label="当前最热门子行业", value=top_sub_ind)
with col3:
    loc_display = "全国"
    if selected_prov != "全国": loc_display = selected_prov
    if selected_city not in ["全市", "请先选择省份"]: loc_display += f" {selected_city}"
    if selected_dist not in ["全区/县", "请先选择城市"]: loc_display += f" {selected_dist}"
    st.metric(label="当前检索区域", value=loc_display)

st.divider()

# 6. 图表与数据明细
col_chart, col_data = st.columns([1, 2])

with col_chart:
    st.markdown("#### 细分赛道 (子行业) 融资分布")
    if not filtered_df.empty:
        # 画图时同样剔除掉没有营养的“未知”分类
        chart_data = filtered_df[filtered_df['子行业'] != '未知']['子行业'].value_counts().head(10)
        st.bar_chart(chart_data)
    else:
        st.info("暂无数据可供生成图表")

with col_data:
    st.markdown("#### 最新企业融资动态")
    filtered_df['完整地址'] = filtered_df.apply(
        lambda row: f"{row['省份']}{row['城市'] if row['省份'] != row['城市'] else ''}{row['区县'] if row['区县'] != '全部' else ''}", 
        axis=1
    )
    
    # ================= 数据表中增加展示“子行业” =================
    display_columns = ['日期', '公司', '行业', '子行业', '融资轮次', '融资金额', '本轮投资方', '完整地址']
    existing_cols = [col for col in display_columns if col in filtered_df.columns]
    
    st.dataframe(filtered_df[existing_cols], use_container_width=True, hide_index=True)

with st.expander("查看当前筛选下的完整原始数据"):
    st.dataframe(filtered_df, use_container_width=True)