from . import stock_recommendation
from flask import request, jsonify
from sqlalchemy import and_
from webapp.models import *
from library.datetime_function import get_offset_open_date_list, get_offset_date
from library.sql_function import sql_to_object, object_to_sql


@stock_recommendation.route('api_trading_point_sorting_aggressive', methods=['GET'])
def api_trading_point_sorting_aggressive():
    date = request.args.get('date')
    date_list = get_offset_open_date_list(date)
    buy_count_data = []
    sell_count_data = []
    category_data = []
    for i in date_list:
        buy_count_data.append(Model_Trading_Point.query.filter_by(trade_date=i, aggressive_buy_point=1).count())
        sell_count_data.append(Model_Trading_Point.query.filter_by(trade_date=i, aggressive_sell_point=1).count())
        category_data.append(i[0:4] + '/' + i[4:6] + '/' + i[6:8])
    model_result = Model_Trading_Point.query.filter_by(trade_date=date, aggressive_buy_point=1).all()
    model_data = []
    for i in model_result:
        code = i.ts_code
        stock_basic = Stock_Basic.query.filter_by(ts_code=code).first()
        stock_bar_result = Stock_Daily_Bar.query.filter(Stock_Daily_Bar.ts_code == code,
                                                        Stock_Daily_Bar.trade_date <= date,
                                                        Stock_Daily_Bar.trade_date >= get_offset_date(date,
                                                                                                      -365)).order_by(
            Stock_Daily_Bar.trade_date.asc()).all()
        close = []
        for j in stock_bar_result:
            close.append(j.close)
        basic_data = Stock_Daily_Basic.query.filter_by(ts_code=code, trade_date=date).first()
        model_data.append(
            {'symbol': stock_basic.symbol, 'name': stock_basic.name, 'bar': close[-60:], 'close': close[-1],
             'min': min(close), 'max': max(close), 'turnover_rate': basic_data.turnover_rate})
    return jsonify(
        {'chart': {'category': category_data, 'buy': buy_count_data, 'sell': sell_count_data}, 'table': model_data})


@stock_recommendation.route('api_trading_point_sorting_steady', methods=['GET'])
def api_trading_point_sorting_steady():
    date = request.args.get('date')
    date_list = get_offset_open_date_list(date)
    buy_count_data = []
    sell_count_data = []
    category_data = []
    for i in date_list:
        buy_count_data.append(Model_Trading_Point.query.filter_by(trade_date=i, steady_buy_point=1).count())
        sell_count_data.append(Model_Trading_Point.query.filter_by(trade_date=i, steady_sell_point=1).count())
        category_data.append(i[0:4] + '/' + i[4:6] + '/' + i[6:8])
    model_result = Model_Trading_Point.query.filter_by(trade_date=date, steady_buy_point=1).all()
    model_data = []
    for i in model_result:
        code = i.ts_code
        stock_basic = Stock_Basic.query.filter_by(ts_code=code).first()
        stock_bar_result = Stock_Daily_Bar.query.filter(Stock_Daily_Bar.ts_code == code,
                                                        Stock_Daily_Bar.trade_date <= date,
                                                        Stock_Daily_Bar.trade_date >= get_offset_date(date,
                                                                                                      -365)).order_by(
            Stock_Daily_Bar.trade_date.asc()).all()
        close = []
        for j in stock_bar_result:
            close.append(j.close)
        basic_data = Stock_Daily_Basic.query.filter_by(ts_code=code, trade_date=date).first()
        model_data.append(
            {'symbol': stock_basic.symbol, 'name': stock_basic.name, 'bar': close[-60:], 'close': close[-1],
             'min': min(close), 'max': max(close), 'turnover_rate': basic_data.turnover_rate})
    return jsonify(
        {'chart': {'category': category_data, 'buy': buy_count_data, 'sell': sell_count_data}, 'table': model_data})


@stock_recommendation.route('api_trading_point_sorting_comprehensive', methods=['GET'])
def api_trading_point_sorting_comprehensive():
    date = request.args.get('date')
    date_list = get_offset_open_date_list(date)
    buy_count_data = []
    sell_count_data = []
    category_data = []
    for i in date_list:
        buy_count_data.append(Model_Trading_Point.query.filter_by(trade_date=i,
                                                                  aggressive_buy_point=1).count() + Model_Trading_Point.query.filter_by(
            trade_date=i, steady_buy_point=1).count())
        sell_count_data.append(Model_Trading_Point.query.filter_by(trade_date=i,
                                                                   aggressive_sell_point=1).count() + Model_Trading_Point.query.filter_by(
            trade_date=i, steady_sell_point=1).count())
        category_data.append(i[0:4] + '/' + i[4:6] + '/' + i[6:8])
    model_aggressive_result = Model_Trading_Point.query.filter_by(trade_date=date, aggressive_buy_point=1).all()
    model_steady_result = Model_Trading_Point.query.filter_by(trade_date=date, steady_buy_point=1).all()
    aggressive_code_list = []
    steady_code_list = []
    for i in model_aggressive_result:
        aggressive_code_list.append(i.ts_code)
    for i in model_steady_result:
        steady_code_list.append(i.ts_code)
    model_common_data = []
    model_aggressive_data = []
    model_steady_data = []
    for i in list(set(aggressive_code_list).intersection(set(steady_code_list))):
        stock_basic = Stock_Basic.query.filter_by(ts_code=i).first()
        bar_data = Stock_Daily_Bar.query.filter_by(ts_code=i, trade_date=date).first()
        basic_data = Stock_Daily_Basic.query.filter_by(ts_code=i, trade_date=date).first()
        model_common_data.append({'symbol': stock_basic.symbol, 'name': stock_basic.name, 'pct_chg': bar_data.pct_chg,
                                  'turnover_rate': basic_data.turnover_rate})
    for i in list(set(aggressive_code_list).difference(set(steady_code_list))):
        stock_basic = Stock_Basic.query.filter_by(ts_code=i).first()
        bar_data = Stock_Daily_Bar.query.filter_by(ts_code=i, trade_date=date).first()
        basic_data = Stock_Daily_Basic.query.filter_by(ts_code=i, trade_date=date).first()
        model_aggressive_data.append(
            {'symbol': stock_basic.symbol, 'name': stock_basic.name, 'pct_chg': bar_data.pct_chg,
             'turnover_rate': basic_data.turnover_rate})
    for i in list(set(steady_code_list).difference(set(aggressive_code_list))):
        stock_basic = Stock_Basic.query.filter_by(ts_code=i).first()
        bar_data = Stock_Daily_Bar.query.filter_by(ts_code=i, trade_date=date).first()
        basic_data = Stock_Daily_Basic.query.filter_by(ts_code=i, trade_date=date).first()
        model_steady_data.append({'symbol': stock_basic.symbol, 'name': stock_basic.name, 'pct_chg': bar_data.pct_chg,
                                  'turnover_rate': basic_data.turnover_rate})
    return jsonify({'chart': {'category': category_data, 'buy': buy_count_data, 'sell': sell_count_data},
                    'table': {'common': model_common_data, 'aggressive': model_aggressive_data,
                              'steady': model_steady_data}})


@stock_recommendation.route('api_similarity_trend_sorting', methods=['GET'])
def api_similarity_trend_sorting():
    date = request.args.get('date')
    model_result = Model_Similarity_Short_Term.query.filter_by(trade_date=date).order_by(
        Model_Similarity_Short_Term.similarity_1_distance.asc()).limit(60).all()
    model_data = []
    for i in model_result:
        match_date = i.similarity_1_matching_end_time
        stock_result = Stock_Basic.query.filter_by(ts_code=i.ts_code).first()
        similar_stock_result = Stock_Basic.query.filter_by(ts_code=i.similarity_1_code).first()
        stock_basic_result = Stock_Daily_Basic.query.filter_by(ts_code=i.ts_code, trade_date=date).first()
        stock_bar = Stock_Daily_Bar.query.filter(Stock_Daily_Bar.ts_code == i.ts_code,
                                                 Stock_Daily_Bar.trade_date <= date).order_by(
            Stock_Daily_Bar.trade_date.desc()).limit(20).all()
        similar_stock_bar = Stock_Daily_Bar.query.filter(Stock_Daily_Bar.ts_code == i.similarity_1_code,
                                                         Stock_Daily_Bar.trade_date >= i.similarity_1_matching_start_time).order_by(
            Stock_Daily_Bar.trade_date.asc()).limit(40).all()
        stock_close_list = []
        similar_stock_close_list = []
        stock_bar.reverse()
        for j in stock_bar:
            stock_close_list.append(j.close)
        stock_close_list.extend(['null'] * 20)
        k = stock_bar[-1].close / similar_stock_bar[19].close
        for j in similar_stock_bar:
            similar_stock_close_list.append(k * j.close)
        model_data.append(
            {'name': stock_result.name, 'symbol': stock_result.symbol, 'similar_name': similar_stock_result.name,
             'similar_symbol': similar_stock_result.symbol,
             'match_date': (match_date[0:4] + '/' + match_date[4:6] + '/' + match_date[6:8]),
             'stock_bar': stock_close_list, 'similar_bar': similar_stock_close_list,
             'turnover_rate': stock_basic_result.turnover_rate})
    return jsonify(model_data)


@stock_recommendation.route('api_correlation_trend_sorting', methods=['GET'])
def api_correlation_trend_sorting():
    date = request.args.get('date')
    model_result = Model_Correlation_Short_Term.query.filter_by(trade_date=date).order_by(
        'ABS(correlation_1_r) DESC').limit(60).all()
    model_data = []
    for i in model_result:
        r = i.correlation_1_r
        match_date = i.correlation_1_matching_end_time
        stock_result = Stock_Basic.query.filter_by(ts_code=i.ts_code).first()
        correlation_stock_result = Stock_Basic.query.filter_by(ts_code=i.correlation_1_code).first()
        stock_basic_result = Stock_Daily_Basic.query.filter_by(ts_code=i.ts_code, trade_date=date).first()
        stock_bar = Stock_Daily_Bar.query.filter(Stock_Daily_Bar.ts_code == i.ts_code,
                                                 Stock_Daily_Bar.trade_date <= date).order_by(
            Stock_Daily_Bar.trade_date.desc()).limit(20).all()
        correlation_stock_bar = Stock_Daily_Bar.query.filter(Stock_Daily_Bar.ts_code == i.correlation_1_code,
                                                             Stock_Daily_Bar.trade_date >= i.correlation_1_matching_start_time).order_by(
            Stock_Daily_Bar.trade_date.asc()).limit(40).all()
        stock_close_list = []
        correlation_stock_close_list = []
        stock_bar.reverse()
        for j in stock_bar:
            stock_close_list.append(j.close)
        stock_close_list.extend(['null'] * 20)
        k = stock_bar[-1].close / correlation_stock_bar[19].close
        for j in correlation_stock_bar:
            correlation_stock_close_list.append(k * j.close)
        model_data.append({'name': stock_result.name, 'symbol': stock_result.symbol,
                           'correlation_name': correlation_stock_result.name,
                           'correlation_symbol': correlation_stock_result.symbol,
                           'match_date': (match_date[0:4] + '/' + match_date[4:6] + '/' + match_date[6:8]),
                           'stock_bar': stock_close_list, 'correlation_bar': correlation_stock_close_list, 'r': r,
                           'turnover_rate': stock_basic_result.turnover_rate})
    return jsonify(model_data)


@stock_recommendation.route('api_history_reappear_sorting', methods=['GET'])
def api_history_reappear_sorting():
    date = request.args.get('date')
    model_result = Model_Similarity_History.query.filter_by(trade_date=date).order_by(
        Model_Similarity_History.distance.asc()).limit(60).all()
    model_data = []
    for i in model_result:
        match_date = i.matching_end_time
        stock_result = Stock_Basic.query.filter_by(ts_code=i.ts_code).first()
        stock_basic_result = Stock_Daily_Basic.query.filter_by(ts_code=i.ts_code, trade_date=date).first()
        stock_bar = Stock_Daily_Bar.query.filter(Stock_Daily_Bar.ts_code == i.ts_code,
                                                 Stock_Daily_Bar.trade_date <= date).order_by(
            Stock_Daily_Bar.trade_date.desc()).limit(30).all()
        similar_stock_bar = Stock_Daily_Bar.query.filter(Stock_Daily_Bar.ts_code == i.ts_code,
                                                         Stock_Daily_Bar.trade_date >= i.matching_start_time).order_by(
            Stock_Daily_Bar.trade_date.asc()).limit(60).all()
        stock_close_list = []
        similar_stock_close_list = []
        stock_bar.reverse()
        for j in stock_bar:
            stock_close_list.append(j.close)
        stock_close_list.extend(['null'] * 30)
        k = stock_bar[-1].close / similar_stock_bar[29].close
        for j in similar_stock_bar:
            similar_stock_close_list.append(k * j.close)
        model_data.append({'name': stock_result.name, 'symbol': stock_result.symbol,
                           'match_date': (match_date[0:4] + '/' + match_date[4:6] + '/' + match_date[6:8]),
                           'stock_bar': stock_close_list, 'similar_bar': similar_stock_close_list,
                           'turnover_rate': stock_basic_result.turnover_rate})
    return jsonify(model_data)


@stock_recommendation.route('api_long_term_trend_sorting', methods=['GET'])
def api_long_term_trend_sorting():
    date = request.args.get('date')
    model_result = Model_State_Transition.query.filter_by(trade_date=date).order_by(
        Model_State_Transition.s_rise_rate.desc()).limit(60).all()
    model_data = []
    for i in model_result:
        stock_result = Stock_Basic.query.filter_by(ts_code=i.ts_code).first()
        stock_basic_result = Stock_Daily_Basic.query.filter_by(ts_code=i.ts_code, trade_date=date).first()
        model_data.append({'name': stock_result.name, 'symbol': stock_result.symbol, 'rise': i.s_rise_rate,
                           'maintain': i.s_maintain_rate, 'fall': i.s_fall_rate,
                           'turnover_rate': stock_basic_result.turnover_rate})
    return jsonify(model_data)


@stock_recommendation.route('api_similarity_eps_sorting', methods=['GET'])
def api_similarity_eps_sorting():
    date = request.args.get('date')
    model_result = Model_Stock_Assessment.query.join(Stock_Daily_Basic,
                                                     and_(Model_Stock_Assessment.ts_code == Stock_Daily_Basic.ts_code,
                                                          Model_Stock_Assessment.trade_date == Stock_Daily_Basic.trade_date)).add_columns(
        Stock_Daily_Basic.pe_ttm).filter_by(trade_date=date).order_by(
        ((Stock_Daily_Basic.pe_ttm - Model_Stock_Assessment.pe_mean) / Model_Stock_Assessment.pe_std).asc()).limit(
        60).all()
    model_data = []
    for i in model_result:
        stock_result = Stock_Basic.query.filter_by(ts_code=i[0].ts_code).first()
        stock_basic_result = Stock_Daily_Basic.query.filter_by(ts_code=i[0].ts_code, trade_date=date).first()
        stock_bar = Stock_Daily_Bar.query.filter(Stock_Daily_Bar.ts_code == i[0].ts_code,
                                                 Stock_Daily_Bar.trade_date <= date).order_by(
            Stock_Daily_Bar.trade_date.desc()).limit(30).all()
        close_list = []
        stock_bar.reverse()
        for j in stock_bar:
            close_list.append(j.close)
        model_data.append(
            {'name': stock_result.name, 'symbol': stock_result.symbol, 'pe_ttm': i.pe_ttm, 'pe_mean': i[0].pe_mean,
             'pe_std': i[0].pe_std, 'close': close_list[-1], 'estimated_value': i[0].estimated_value,
             'turnover_rate': stock_basic_result.turnover_rate, 'scale': (i.pe_ttm - i[0].pe_mean) / i[0].pe_std,
             'stock_bar': close_list})
    return jsonify(model_data)


@stock_recommendation.route('api_industry_csrc_mean_sorting', methods=['GET'])
def api_industry_csrc_mean_sorting():
    date = request.args.get('date')
    model_result = Stock_Daily_Basic.query.join(Stock_Company_Extend,
                                                Stock_Daily_Basic.ts_code == Stock_Company_Extend.ts_code).add_columns(
        Stock_Company_Extend.industry_csrc_name).join(Stock_Industry_CSRC_2,
                                                      Stock_Company_Extend.industry_csrc_code == Stock_Industry_CSRC_2.industry_csrc_2_code).join(
        Stock_Industry_CSRC_1, Stock_Industry_CSRC_1.industry_csrc_1_code == Stock_Industry_CSRC_2.belong_to).join(
        Stock_Industry_Basic, and_(Stock_Industry_CSRC_1.industry_csrc_1_code == Stock_Industry_Basic.industry_code,
                                   Stock_Daily_Basic.trade_date == Stock_Industry_Basic.trade_date)).add_columns(
        Stock_Industry_Basic.pe_ttm_overall).filter_by(trade_date=date).order_by(
        ((Stock_Daily_Basic.pe_ttm - Stock_Industry_Basic.pe_ttm_overall) / Stock_Daily_Basic.pe_ttm).asc()).limit(
        60).all()
    model_data = []
    for i in model_result:
        stock_result = Stock_Basic.query.filter_by(ts_code=i[0].ts_code).first()
        stock_bar = Stock_Daily_Bar.query.filter(Stock_Daily_Bar.ts_code == i[0].ts_code,
                                                 Stock_Daily_Bar.trade_date <= date).order_by(
            Stock_Daily_Bar.trade_date.desc()).limit(30).all()
        close_list = []
        stock_bar.reverse()
        for j in stock_bar:
            close_list.append(j.close)
        model_data.append({'name': stock_result.name, 'symbol': stock_result.symbol, 'pe_ttm': i[0].pe_ttm,
                           'industry': i.industry_csrc_name, 'industry_pe_mean': i.pe_ttm_overall,
                           'turnover_rate': i[0].turnover_rate, 'scale': (i[0].pe_ttm - i.pe_ttm_overall) / i[0].pe_ttm,
                           'stock_bar': close_list})
    return jsonify(model_data)


@stock_recommendation.route('api_industry_sw_mean_sorting', methods=['GET'])
def api_industry_sw_mean_sorting():
    date = request.args.get('date')
    model_result = Stock_Daily_Basic.query.join(Stock_Company_Extend,
                                                Stock_Daily_Basic.ts_code == Stock_Company_Extend.ts_code).add_columns(
        Stock_Company_Extend.industry_sw_name).join(Stock_Industry_SW_3,
                                                    Stock_Company_Extend.industry_sw_code == Stock_Industry_SW_3.industry_sw_3_code).join(
        Stock_Industry_SW_2, Stock_Industry_SW_3.belong_to == Stock_Industry_SW_2.industry_sw_2_code).join(
        Stock_Industry_SW_1, Stock_Industry_SW_2.belong_to == Stock_Industry_SW_1.industry_sw_1_code).join(
        Stock_Industry_Basic, and_(Stock_Industry_SW_1.industry_sw_1_code == Stock_Industry_Basic.industry_code,
                                   Stock_Daily_Basic.trade_date == Stock_Industry_Basic.trade_date)).add_columns(
        Stock_Industry_Basic.pe_ttm_overall).filter_by(trade_date=date).order_by(
        ((Stock_Daily_Basic.pe_ttm - Stock_Industry_Basic.pe_ttm_overall) / Stock_Daily_Basic.pe_ttm).asc()).limit(
        60).all()
    model_data = []
    for i in model_result:
        stock_result = Stock_Basic.query.filter_by(ts_code=i[0].ts_code).first()
        stock_bar = Stock_Daily_Bar.query.filter(Stock_Daily_Bar.ts_code == i[0].ts_code,
                                                 Stock_Daily_Bar.trade_date <= date).order_by(
            Stock_Daily_Bar.trade_date.desc()).limit(30).all()
        close_list = []
        stock_bar.reverse()
        for j in stock_bar:
            close_list.append(j.close)
        model_data.append({'name': stock_result.name, 'symbol': stock_result.symbol, 'pe_ttm': i[0].pe_ttm,
                           'industry': i.industry_sw_name, 'industry_pe_mean': i.pe_ttm_overall,
                           'turnover_rate': i[0].turnover_rate, 'scale': (i[0].pe_ttm - i.pe_ttm_overall) / i[0].pe_ttm,
                           'stock_bar': close_list})
    return jsonify(model_data)


@stock_recommendation.route('api_industry_csrc_pe_sorting', methods=['GET'])
def api_industry_csrc_pe_sorting():
    date = request.args.get('date')
    industry_list = []
    industry_code_list = []
    csrc_1_result = Stock_Industry_CSRC_1.query.all()
    for i in csrc_1_result:
        csrc_2_result = Stock_Industry_CSRC_2.query.filter_by(belong_to=i.industry_csrc_1_code).all()
        sub_list = []
        sub_code_list = []
        for j in csrc_2_result:
            sub_list.append(j.industry_csrc_2_name)
            sub_code_list.append(j.industry_csrc_2_code)
        industry_list.append({'name': i.industry_csrc_1_name, 'sub': sub_list})
        industry_code_list.append({'code': i.industry_csrc_1_code, 'sub_code': sub_code_list})
    model_data = []
    for i in industry_code_list:
        sub_model_data = []
        for j in i['sub_code']:
            order_result = Stock_Daily_Basic.query.join(Stock_Company_Extend,
                                                        Stock_Daily_Basic.ts_code == Stock_Company_Extend.ts_code).join(
                Stock_Industry_CSRC_2,
                Stock_Company_Extend.industry_csrc_code == Stock_Industry_CSRC_2.industry_csrc_2_code).join(
                Stock_Industry_CSRC_1,
                Stock_Industry_CSRC_1.industry_csrc_1_code == Stock_Industry_CSRC_2.belong_to).join(
                Stock_Industry_Basic,
                and_(Stock_Industry_CSRC_1.industry_csrc_1_code == Stock_Industry_Basic.industry_code,
                     Stock_Daily_Basic.trade_date == Stock_Industry_Basic.trade_date)).add_columns(
                Stock_Industry_Basic.pe_avg, Stock_Industry_Basic.pe_ttm_overall,
                Stock_Industry_Basic.csrc_company_num).filter(Stock_Daily_Basic.trade_date == date,
                                                              Stock_Industry_CSRC_2.industry_csrc_2_code == j).order_by(
                Stock_Daily_Basic.pe_ttm.asc()).limit(3).all()
            order_data = []
            if order_result != []:
                for x in order_result:
                    order_data.append(
                        {'name': Stock_Basic.query.filter_by(ts_code=x[0].ts_code).first().name, 'pe_ttm': x[0].pe_ttm})
                sub_model_data.append({'company_num': order_result[0].csrc_company_num, 'pe': order_result[0].pe_avg,
                                       'pe_ttm': order_result[0].pe_ttm_overall, 'order': order_data})
        order_result = Stock_Daily_Basic.query.join(Stock_Company_Extend,
                                                    Stock_Daily_Basic.ts_code == Stock_Company_Extend.ts_code).join(
            Stock_Industry_CSRC_2,
            Stock_Company_Extend.industry_csrc_code == Stock_Industry_CSRC_2.industry_csrc_2_code).join(
            Stock_Industry_CSRC_1,
            Stock_Industry_CSRC_1.industry_csrc_1_code == Stock_Industry_CSRC_2.belong_to).join(
            Stock_Industry_Basic,
            and_(Stock_Industry_CSRC_1.industry_csrc_1_code == Stock_Industry_Basic.industry_code,
                 Stock_Daily_Basic.trade_date == Stock_Industry_Basic.trade_date)).add_columns(
            Stock_Industry_Basic.pe_avg, Stock_Industry_Basic.pe_ttm_overall,
            Stock_Industry_Basic.csrc_company_num).filter(Stock_Daily_Basic.trade_date == date,
                                                          Stock_Industry_CSRC_1.industry_csrc_1_code == i[
                                                              'code']).order_by(
            Stock_Daily_Basic.pe_ttm.asc()).limit(3).all()
        order_data = []
        if order_result != []:
            for x in order_result:
                order_data.append(
                    {'name': Stock_Basic.query.filter_by(ts_code=x[0].ts_code).first().name, 'pe_ttm': x[0].pe_ttm})
            model_data.append({'company_num': order_result[0].csrc_company_num, 'pe': order_result[0].pe_avg,
                               'pe_ttm': order_result[0].pe_ttm_overall, 'order': order_data, 'sub': sub_model_data})
    return jsonify({'industry': industry_list, 'data': model_data})


@stock_recommendation.route('api_industry_sw_pe_sorting', methods=['GET'])
def api_industry_sw_pe_sorting():
    date = request.args.get('date')
    industry_list = []
    industry_code_list = []
    sw_1_result = Stock_Industry_SW_1.query.all()
    for i in sw_1_result:
        sw_2_result = Stock_Industry_SW_2.query.filter_by(belong_to=i.industry_sw_1_code).all()
        sub_list = []
        sub_code_list = []
        for j in sw_2_result:
            sub_list.append(j.industry_sw_2_name)
            sub_code_list.append(j.industry_sw_2_code)
        industry_list.append({'name': i.industry_sw_1_name, 'sub': sub_list})
        industry_code_list.append({'code': i.industry_sw_1_code, 'sub_code': sub_code_list})
    model_data = []
    for i in industry_code_list:
        sub_model_data = []
        for j in i['sub_code']:
            order_result = Stock_Daily_Basic.query.join(Stock_Company_Extend,
                                                        Stock_Daily_Basic.ts_code == Stock_Company_Extend.ts_code).join(
                Stock_Industry_SW_3,
                Stock_Company_Extend.industry_sw_code == Stock_Industry_SW_3.industry_sw_3_code).join(
                Stock_Industry_SW_2, Stock_Industry_SW_3.belong_to == Stock_Industry_SW_2.industry_sw_2_code).join(
                Stock_Industry_SW_1, Stock_Industry_SW_2.belong_to == Stock_Industry_SW_1.industry_sw_1_code).join(
                Stock_Industry_Basic,
                and_(Stock_Industry_SW_1.industry_sw_1_code == Stock_Industry_Basic.industry_code,
                     Stock_Daily_Basic.trade_date == Stock_Industry_Basic.trade_date)).add_columns(
                Stock_Industry_Basic.pe_avg, Stock_Industry_Basic.pe_ttm_overall,
                Stock_Industry_Basic.csrc_company_num).filter(Stock_Daily_Basic.trade_date == date,
                                                              Stock_Industry_SW_2.industry_sw_2_code == j).order_by(
                Stock_Daily_Basic.pe_ttm.asc()).limit(3).all()
            order_data = []
            if order_result != []:
                for x in order_result:
                    order_data.append(
                        {'name': Stock_Basic.query.filter_by(ts_code=x[0].ts_code).first().name, 'pe_ttm': x[0].pe_ttm})
                sub_model_data.append({'company_num': order_result[0].csrc_company_num, 'pe': order_result[0].pe_avg,
                                       'pe_ttm': order_result[0].pe_ttm_overall, 'order': order_data})
        order_result = Stock_Daily_Basic.query.join(Stock_Company_Extend,
                                                    Stock_Daily_Basic.ts_code == Stock_Company_Extend.ts_code).join(
            Stock_Industry_SW_3, Stock_Company_Extend.industry_sw_code == Stock_Industry_SW_3.industry_sw_3_code).join(
            Stock_Industry_SW_2, Stock_Industry_SW_3.belong_to == Stock_Industry_SW_2.industry_sw_2_code).join(
            Stock_Industry_SW_1, Stock_Industry_SW_2.belong_to == Stock_Industry_SW_1.industry_sw_1_code).join(
            Stock_Industry_Basic,
            and_(Stock_Industry_SW_1.industry_sw_1_code == Stock_Industry_Basic.industry_code,
                 Stock_Daily_Basic.trade_date == Stock_Industry_Basic.trade_date)).add_columns(
            Stock_Industry_Basic.pe_avg, Stock_Industry_Basic.pe_ttm_overall,
            Stock_Industry_Basic.csrc_company_num).filter(Stock_Daily_Basic.trade_date == date,
                                                          Stock_Industry_SW_1.industry_sw_1_code == i['code']).order_by(
            Stock_Daily_Basic.pe_ttm.asc()).limit(3).all()
        order_data = []
        if order_result != []:
            for x in order_result:
                order_data.append(
                    {'name': Stock_Basic.query.filter_by(ts_code=x[0].ts_code).first().name, 'pe_ttm': x[0].pe_ttm})
            model_data.append({'company_num': order_result[0].csrc_company_num, 'pe': order_result[0].pe_avg,
                               'pe_ttm': order_result[0].pe_ttm_overall, 'order': order_data, 'sub': sub_model_data})
    return jsonify({'industry': industry_list, 'data': model_data})


@stock_recommendation.route('api_main_capital', methods=['GET'])
def api_main_capital():
    date = request.args.get('date')
    model_result=Market_Money_Flow.query.filter_by(trade_date=date).order_by(((Market_Money_Flow.buy_lg_amount+Market_Money_Flow.sell_lg_amount+Market_Money_Flow.buy_elg_amount+Market_Money_Flow.sell_elg_amount)/(Market_Money_Flow.buy_lg_amount+Market_Money_Flow.sell_lg_amount+Market_Money_Flow.buy_elg_amount+Market_Money_Flow.sell_elg_amount+Market_Money_Flow.buy_md_amount+Market_Money_Flow.sell_md_amount+Market_Money_Flow.buy_sm_amount+Market_Money_Flow.sell_sm_amount)).desc()).limit(60).all()
    model_data=[]
    for i in model_result:
        stock_result = Stock_Basic.query.filter_by(ts_code=i.ts_code).first()
        stock_basic_result = Stock_Daily_Basic.query.filter_by(ts_code=i.ts_code, trade_date=date).first()
        stock_bar = Stock_Daily_Bar.query.filter(Stock_Daily_Bar.ts_code == i.ts_code,
                                                 Stock_Daily_Bar.trade_date <= date).order_by(
            Stock_Daily_Bar.trade_date.desc()).limit(30).all()
        close_list = []
        stock_bar.reverse()
        for j in stock_bar:
            close_list.append(j.close)
        model_data.append({'name':stock_result.name,'symbol':stock_result.symbol,'main_capital':i.buy_lg_amount+i.sell_lg_amount+i.buy_elg_amount+i.sell_elg_amount,'total_capital':i.buy_lg_amount+i.sell_lg_amount+i.buy_elg_amount+i.sell_elg_amount+i.buy_md_amount+i.sell_md_amount+i.buy_sm_amount+i.sell_sm_amount,'pct_chg':stock_bar[-1].pct_chg,'turnover_rate':stock_basic_result.turnover_rate,'close_list':close_list})
    return jsonify(model_data)

@stock_recommendation.route('api_main_net', methods=['GET'])
def api_main_net():
    date = request.args.get('date')
    model_result=Market_Money_Flow.query.filter_by(trade_date=date).order_by(((Market_Money_Flow.buy_lg_amount-Market_Money_Flow.sell_lg_amount+Market_Money_Flow.buy_elg_amount-Market_Money_Flow.sell_elg_amount)/(Market_Money_Flow.buy_lg_amount+Market_Money_Flow.sell_lg_amount+Market_Money_Flow.buy_elg_amount+Market_Money_Flow.sell_elg_amount+Market_Money_Flow.buy_md_amount+Market_Money_Flow.sell_md_amount+Market_Money_Flow.buy_sm_amount+Market_Money_Flow.sell_sm_amount)).desc()).limit(60).all()
    model_data=[]
    for i in model_result:
        stock_result = Stock_Basic.query.filter_by(ts_code=i.ts_code).first()
        stock_basic_result = Stock_Daily_Basic.query.filter_by(ts_code=i.ts_code, trade_date=date).first()
        stock_bar = Stock_Daily_Bar.query.filter(Stock_Daily_Bar.ts_code == i.ts_code,
                                                 Stock_Daily_Bar.trade_date <= date).order_by(
            Stock_Daily_Bar.trade_date.desc()).limit(30).all()
        close_list = []
        stock_bar.reverse()
        for j in stock_bar:
            close_list.append(j.close)
        model_data.append({'name':stock_result.name,'symbol':stock_result.symbol,'main_net':i.buy_lg_amount-i.sell_lg_amount+i.buy_elg_amount-i.sell_elg_amount,'total_capital':i.buy_lg_amount+i.sell_lg_amount+i.buy_elg_amount+i.sell_elg_amount+i.buy_md_amount+i.sell_md_amount+i.buy_sm_amount+i.sell_sm_amount,'pct_chg':stock_bar[-1].pct_chg,'turnover_rate':stock_basic_result.turnover_rate,'close_list':close_list})
    return jsonify(model_data)

@stock_recommendation.route('api_main_ability', methods=['GET'])
def api_main_ability():
    date = request.args.get('date')
    model_result = Market_Money_Flow.query.join(Stock_Daily_Basic,and_(Market_Money_Flow.ts_code==Stock_Daily_Basic.ts_code,Market_Money_Flow.trade_date==Stock_Daily_Basic.trade_date)).add_columns(Stock_Daily_Basic.circ_mv,Stock_Daily_Basic.turnover_rate).join(Stock_Daily_Bar,and_(Market_Money_Flow.ts_code==Stock_Daily_Bar.ts_code,Market_Money_Flow.trade_date==Stock_Daily_Bar.trade_date)).add_columns(Stock_Daily_Bar.pct_chg).filter_by(trade_date=date).order_by(((Market_Money_Flow.net_mf_amount/(Stock_Daily_Basic.circ_mv/(1+Stock_Daily_Bar.pct_chg)*Stock_Daily_Bar.pct_chg))/((Market_Money_Flow.buy_lg_amount + Market_Money_Flow.sell_lg_amount + Market_Money_Flow.buy_elg_amount + Market_Money_Flow.sell_elg_amount) / (Market_Money_Flow.buy_lg_amount + Market_Money_Flow.sell_lg_amount + Market_Money_Flow.buy_elg_amount + Market_Money_Flow.sell_elg_amount + Market_Money_Flow.buy_md_amount + Market_Money_Flow.sell_md_amount + Market_Money_Flow.buy_sm_amount + Market_Money_Flow.sell_sm_amount))).desc()).limit(60).all()
    model_data=[]
    for i in model_result:
        stock_result = Stock_Basic.query.filter_by(ts_code=i[0].ts_code).first()
        stock_bar = Stock_Daily_Bar.query.filter(Stock_Daily_Bar.ts_code == i[0].ts_code,
                                                 Stock_Daily_Bar.trade_date <= date).order_by(
            Stock_Daily_Bar.trade_date.desc()).limit(30).all()
        close_list = []
        stock_bar.reverse()
        for j in stock_bar:
            close_list.append(j.close)
        model_data.append({'name':stock_result.name,'symbol':stock_result.symbol,'main_ratio':(i[0].buy_lg_amount+i[0].sell_lg_amount+i[0].buy_elg_amount+i[0].sell_elg_amount)/(i[0].buy_lg_amount+i[0].sell_lg_amount+i[0].buy_elg_amount+i[0].sell_elg_amount+i[0].buy_md_amount+i[0].sell_md_amount+i[0].buy_sm_amount+i[0].sell_sm_amount),'corr':(i[0].net_mf_amount/(i.circ_mv/(1+i.pct_chg)*i.pct_chg)),'pct_chg':stock_bar[-1].pct_chg,'turnover_rate':i.turnover_rate,'close_list':close_list})
    return jsonify(model_data)


@stock_recommendation.route('api_associate_rule_sorting', methods=['GET'])
def api_associate_rule_sorting():
    date = request.args.get('date')
    rise_rise_data = []
    rise_rise_result = Model_Associate_Rule.query.filter(Model_Associate_Rule.trade_date == date,
                                 Model_Associate_Rule.associate_type == 'rise_rise').order_by(
        Model_Associate_Rule.probability.desc()).all()
    for i in rise_rise_result:
        stock_result=Stock_Basic.query.filter_by(ts_code=i.ts_code).first()
        associate_stock_result=Stock_Basic.query.filter_by(ts_code=i.associate_code).first()
        rise_rise_data.append([associate_stock_result.name, i.approval_rating, i.probability,
                               i.trading_day_count, i.matching_day_count,
                               i.effect_day_count,stock_result.name])
    rise_fall_data = []
    rise_fall_result = Model_Associate_Rule.query.filter(Model_Associate_Rule.trade_date == date,
                                 Model_Associate_Rule.associate_type == 'rise_fall').order_by(
        Model_Associate_Rule.probability.desc()).all()
    for i in rise_fall_result:
        stock_result=Stock_Basic.query.filter_by(ts_code=i.ts_code).first()
        associate_stock_result=Stock_Basic.query.filter_by(ts_code=i.associate_code).first()
        rise_fall_data.append([associate_stock_result.name, i.approval_rating, i.probability,
                               i.trading_day_count, i.matching_day_count,
                               i.effect_day_count,stock_result.name])
    rise_not_rise_data = []
    rise_not_rise_result = Model_Associate_Rule.query.filter(Model_Associate_Rule.trade_date == date,
                                 Model_Associate_Rule.associate_type == 'rise_not_rise').order_by(
        Model_Associate_Rule.probability.desc()).all()
    for i in rise_not_rise_result:
        stock_result=Stock_Basic.query.filter_by(ts_code=i.ts_code).first()
        associate_stock_result=Stock_Basic.query.filter_by(ts_code=i.associate_code).first()
        rise_not_rise_data.append([associate_stock_result.name, i.approval_rating, i.probability,
                               i.trading_day_count, i.matching_day_count,
                               i.effect_day_count,stock_result.name])
    rise_not_fall_data = []
    rise_not_fall_result = Model_Associate_Rule.query.filter(Model_Associate_Rule.trade_date == date,
                                 Model_Associate_Rule.associate_type == 'rise_not_fall').order_by(
        Model_Associate_Rule.probability.desc()).all()
    for i in rise_not_fall_result:
        stock_result=Stock_Basic.query.filter_by(ts_code=i.ts_code).first()
        associate_stock_result=Stock_Basic.query.filter_by(ts_code=i.associate_code).first()
        rise_not_fall_data.append([associate_stock_result.name, i.approval_rating, i.probability,
                               i.trading_day_count, i.matching_day_count,
                               i.effect_day_count,stock_result.name])
    fall_rise_data = []
    fall_rise_result = Model_Associate_Rule.query.filter(Model_Associate_Rule.trade_date == date,
                                 Model_Associate_Rule.associate_type == 'fall_rise').order_by(
        Model_Associate_Rule.probability.desc()).all()
    for i in fall_rise_result:
        stock_result=Stock_Basic.query.filter_by(ts_code=i.ts_code).first()
        associate_stock_result=Stock_Basic.query.filter_by(ts_code=i.associate_code).first()
        fall_rise_data.append([associate_stock_result.name, i.approval_rating, i.probability,
                               i.trading_day_count, i.matching_day_count,
                               i.effect_day_count,stock_result.name])
    fall_fall_data = []
    fall_fall_result = Model_Associate_Rule.query.filter(Model_Associate_Rule.trade_date == date,
                                 Model_Associate_Rule.associate_type == 'fall_fall').order_by(
        Model_Associate_Rule.probability.desc()).all()
    for i in fall_fall_result:
        stock_result=Stock_Basic.query.filter_by(ts_code=i.ts_code).first()
        associate_stock_result=Stock_Basic.query.filter_by(ts_code=i.associate_code).first()
        fall_fall_data.append([associate_stock_result.name, i.approval_rating, i.probability,
                               i.trading_day_count, i.matching_day_count,
                               i.effect_day_count,stock_result.name])
    fall_not_rise_data = []
    fall_not_rise_result = Model_Associate_Rule.query.filter(Model_Associate_Rule.trade_date == date,
                                 Model_Associate_Rule.associate_type == 'fall_not_rise').order_by(
        Model_Associate_Rule.probability.desc()).all()
    for i in fall_not_rise_result:
        stock_result=Stock_Basic.query.filter_by(ts_code=i.ts_code).first()
        associate_stock_result=Stock_Basic.query.filter_by(ts_code=i.associate_code).first()
        fall_not_rise_data.append([associate_stock_result.name, i.approval_rating, i.probability,
                               i.trading_day_count, i.matching_day_count,
                               i.effect_day_count,stock_result.name])
    fall_not_fall_data = []
    fall_not_fall_result = Model_Associate_Rule.query.filter(Model_Associate_Rule.trade_date == date,
                                 Model_Associate_Rule.associate_type == 'fall_not_fall').order_by(
        Model_Associate_Rule.probability.desc()).all()
    for i in fall_not_fall_result:
        stock_result=Stock_Basic.query.filter_by(ts_code=i.ts_code).first()
        associate_stock_result=Stock_Basic.query.filter_by(ts_code=i.associate_code).first()
        fall_not_fall_data.append([associate_stock_result.name, i.approval_rating, i.probability,
                               i.trading_day_count, i.matching_day_count,
                               i.effect_day_count,stock_result.name])
    model_data = {'rise_rise': rise_rise_data, 'rise_fall': rise_fall_data,
                           'rise_not_rise': rise_not_rise_data, 'rise_not_fall': rise_not_fall_data,
                           'fall_rise': fall_rise_data, 'fall_fall': fall_fall_data,
                           'fall_not_rise': fall_not_rise_data, 'fall_not_fall': fall_not_fall_data}
    return jsonify(model_data)


@stock_recommendation.route('api_fluctuation_combination_sorting', methods=['GET'])
def api_fluctuation_combination_sorting():
    date = request.args.get('date')
    pass


@stock_recommendation.route('api_fluctuation_sequencing_sorting', methods=['GET'])
def api_fluctuation_sequencing_sorting():
    date = request.args.get('date')
    high_change_list=[]
    high_change_result=Model_Fluctuation_Sequencing.query.filter_by(trade_date=date).all()
    for i in high_change_result:
        high_change_list.append(int(i.high_change*100+0.5))
    high_change_statistics=[0]*101
    for i in high_change_list:
        high_change_statistics[100+i]+=1
    model_result=Model_Fluctuation_Sequencing.query.filter_by(trade_date=date).order_by(Model_Fluctuation_Sequencing.high_order.asc()).limit(60).all()
    model_data=[]
    for i in model_result:
        stock_result=Stock_Basic.query.filter_by(ts_code=i.ts_code).first()
        model_data.append({'name':stock_result.name,'symbol':stock_result.symbol,'close':i.close,'high_change':i.high_change,'high_order':i.high_order,'low_change':i.low_change,'low_order':i.low_order,'order_sum':i.order_sum})
    return jsonify({'chart':high_change_statistics,'table':model_data})


@stock_recommendation.route('api_shape_matching_sorting', methods=['GET'])
def api_shape_matching_sorting():
    date = request.args.get('date')
    pass

