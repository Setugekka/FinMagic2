from . import stock_recommendation
from flask import render_template, request, abort
from library.datetime_function import date_validation


@stock_recommendation.route('trend_prediction_sorting/trading_point_sorting', methods=['GET'])
def trading_point_sorting():
    date = request.args.get('date')
    mode = request.args.get('mode')
    if mode is None:
        mode='0'
    date_validated, date_list = date_validation(date)
    if mode == '0':
        return render_template(
            'stock_recommendation/stock_sorting/trend_prediction_sorting/trading_point_sorting_aggressive.html',
            date=date_validated,date_list=date_list)
    elif mode == '1':
        return render_template(
            'stock_recommendation/stock_sorting/trend_prediction_sorting/trading_point_sorting_steady.html',
            date=date_validated, date_list=date_list)
    elif mode == '2':
        return render_template(
            'stock_recommendation/stock_sorting/trend_prediction_sorting/trading_point_sorting_comprehensive.html',
            date=date_validated,date_list=date_list)
    else:
        abort(400)

@stock_recommendation.route('trend_prediction_sorting/similarity_trend_sorting', methods=['GET'])
def similarity_trend_sorting():
    date = request.args.get('date')
    date_validated, date_list = date_validation(date)
    return render_template('stock_recommendation/stock_sorting/trend_prediction_sorting/similarity_trend_sorting.html',
            date=date_validated, date_list=date_list)

@stock_recommendation.route('trend_prediction_sorting/correlation_trend_sorting', methods=['GET'])
def correlation_trend_sorting():
    date = request.args.get('date')
    date_validated, date_list = date_validation(date)
    return render_template('stock_recommendation/stock_sorting/trend_prediction_sorting/correlation_trend_sorting.html',
            date=date_validated, date_list=date_list)

@stock_recommendation.route('trend_prediction_sorting/history_reappear_sorting', methods=['GET'])
def history_reappear_sorting():
    date = request.args.get('date')
    date_validated, date_list = date_validation(date)
    return render_template('stock_recommendation/stock_sorting/trend_prediction_sorting/history_reappear_sorting.html',
            date=date_validated, date_list=date_list)

@stock_recommendation.route('trend_prediction_sorting/long_term_trend_sorting', methods=['GET'])
def long_term_trend_sorting():
    date = request.args.get('date')
    date_validated, date_list = date_validation(date)
    return render_template('stock_recommendation/stock_sorting/trend_prediction_sorting/long_term_trend_sorting.html',
            date=date_validated, date_list=date_list)



@stock_recommendation.route('stock_assessment_sorting/similarity_eps_sorting', methods=['GET'])
def similarity_eps_sorting():
    date = request.args.get('date')
    date_validated, date_list = date_validation(date)
    return render_template('stock_recommendation/stock_sorting/stock_assessment_sorting/similarity_eps_sorting.html',
            date=date_validated, date_list=date_list)

@stock_recommendation.route('stock_assessment_sorting/industry_mean_sorting', methods=['GET'])
def industry_mean_sorting():
    date = request.args.get('date')
    mode = request.args.get('mode')
    if mode is None:
        mode='0'
    date_validated, date_list = date_validation(date)
    if mode == '0':
        return render_template(
            'stock_recommendation/stock_sorting/stock_assessment_sorting/industry_csrc_mean_sorting.html',
            date=date_validated,date_list=date_list)
    elif mode == '1':
        return render_template(
            'stock_recommendation/stock_sorting/stock_assessment_sorting/industry_sw_mean_sorting.html',
            date=date_validated, date_list=date_list)
    else:
        abort(400)

@stock_recommendation.route('stock_assessment_sorting/industry_pe_sorting', methods=['GET'])
def industry_pe_sorting():
    date = request.args.get('date')
    mode = request.args.get('mode')
    if mode is None:
        mode='0'
    date_validated, date_list = date_validation(date)
    if mode == '0':
        return render_template(
            'stock_recommendation/stock_sorting/stock_assessment_sorting/industry_csrc_pe_sorting.html',
            date=date_validated,date_list=date_list)
    elif mode == '1':
        return render_template(
            'stock_recommendation/stock_sorting/stock_assessment_sorting/industry_sw_pe_sorting.html',
            date=date_validated, date_list=date_list)
    else:
        abort(400)



@stock_recommendation.route('money_flow_sorting/main_capital', methods=['GET'])
def main_capital():
    date = request.args.get('date')
    date_validated, date_list = date_validation(date)
    return render_template('stock_recommendation/stock_sorting/money_flow_sorting/main_capital.html',
            date=date_validated, date_list=date_list)

@stock_recommendation.route('money_flow_sorting/main_net', methods=['GET'])
def main_net():
    date = request.args.get('date')
    date_validated, date_list = date_validation(date)
    return render_template('stock_recommendation/stock_sorting/money_flow_sorting/main_net.html',
            date=date_validated, date_list=date_list)

@stock_recommendation.route('money_flow_sorting/main_ability', methods=['GET'])
def main_ability():
    date = request.args.get('date')
    date_validated, date_list = date_validation(date)
    return render_template('stock_recommendation/stock_sorting/money_flow_sorting/main_ability.html',
            date=date_validated, date_list=date_list)



# 筹码分布排序
@stock_recommendation.route('chips_distribution_sorting', methods=['GET'])
def chips_distribution_sorting():
    pass


#规则统计排序
@stock_recommendation.route('rule_statistics_sorting/associate_rule_sorting', methods=['GET'])
def associate_rule_sorting():
    date = request.args.get('date')
    date_validated, date_list = date_validation(date)
    return render_template('stock_recommendation/stock_sorting/rule_statistics_sorting/associate_rule_sorting.html',
            date=date_validated, date_list=date_list)

@stock_recommendation.route('rule_statistics_sorting/fluctuation_combination_sorting', methods=['GET'])
def fluctuation_combination_sorting():
    date = request.args.get('date')
    date_validated, date_list = date_validation(date)
    return render_template('stock_recommendation/stock_sorting/rule_statistics_sorting/fluctuation_combination_sorting.html',
            date=date_validated, date_list=date_list)

@stock_recommendation.route('rule_statistics_sorting/fluctuation_sequencing_sorting', methods=['GET'])
def fluctuation_sequencing_sorting():
    date = request.args.get('date')
    date_validated, date_list = date_validation(date)
    return render_template('stock_recommendation/stock_sorting/rule_statistics_sorting/fluctuation_sequencing_sorting.html',
            date=date_validated, date_list=date_list)

@stock_recommendation.route('rule_statistics_sorting/shape_matching_sorting', methods=['GET'])
def shape_matching_sorting():
    date = request.args.get('date')
    date_validated, date_list = date_validation(date)
    return render_template('stock_recommendation/stock_sorting/rule_statistics_sorting/shape_matching_sorting.html',
            date=date_validated, date_list=date_list)



# 人气热度排序
@stock_recommendation.route('popularity_heat_sorting')
def popularity_heat_sorting():
    pass