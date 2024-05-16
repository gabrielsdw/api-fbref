from flask import Flask, jsonify
from service.db import MongoDbAtlasService
from unidecode import unidecode

app = Flask(__name__)

db = MongoDbAtlasService('gabrielsdw', '54321', 'fbref')

PREMIERLEAGUE_TEAMS = ['aek_athens', 'ajax', 'arsenal', 'aston_villa', 'atalanta', 'az_alkmaar', 'bayer_leverkusen', 'bayern_munich', 'blackburn_rovers', 'blackpool', 'bolton_wanderers', 'bournemouth', 'brentford', 'brighton_&_hove_albion', 'bristol_city', 'burnley', 'chelsea', 'coventry_city', 'crystal_palace', 'doncaster_rovers', 'dortmund', 'everton', 'exeter_city', 'fc_copenhagen', 'freiburg', 'fulham', 'galatasaray', 'gillingham', 'hibernian', 'ipswich_town', 'lask', 'legia_warsaw', 'lens', 'lille', 'lincoln_city', 'liverpool', 'luton_town', 
'manchester_city', 'manchester_united', 'marseille', 'middlesbrough', 'milan', 'newcastle_united', 'newport_county', 'nottingham_forest', 'olympiacos', 'paris_saint-germain', 'plymouth_argyle', 'porto', 'psv_eindhoven', 'queens_park_rangers', 'rb_leipzig', 'real_madrid', 'red_star_belgrade', 'roma', 'salford_city', 'sevilla', 'sheffield_united', 'sparta_prague', 'stoke_city', 'sunderland', 'swansea_city', 'tottenham_hotspur', 'toulouse', 'tsc_backa_top', 'union_sg', 'west_bromwich_albion', 'west_ham_united', 'wigan_athletic', 'wolverhampton_wanderers', 'young_boys', 'zrinjski_mostar']

LALIGA_TEAMS = ['alaves', 'almeria', 'amorebieta', 'andratx', 'antwerp', 'arandina', 'aris_limassol_fc', 'arosa', 'arsenal', 'athletic_club', 'atletico_astorga', 'atletico_de_lugones', 'atletico_madrid', 'atzeneta', 'barbastro', 'barcelona', 'bayern_munich', 'benfica', 'boiro', 'braga', 'bunol', 'burgos', 'cadiz', 'cartagena', 'castellon', 'cayon', 'cd_san_roque_de_lepe', 'celta_vigo', 'celtic', 'cf_talavera_de_la_reina', 'chiclana', 'club_brugge', 'deportivo_murcia', 'dinamo_zagreb', 'dortmund', 'eibar', 'elche', 'espanyol', 'feyenoord', 'getafe', 'girona', 'granada', 'hernan_cortes', 'huesca', 'internazionale', 'las_palmas', 'lazio', 'lens', 'llagostera', 'lugo', 'maccabi_haifa', 'malaga', 'mallorca', 'manacor', 'manchester_city', 'marseille', 'napoli', 'orihuela', 'osasuna', 'panathinaikos', 'paris_saint-germain', 'porto', 'psv_eindhoven', 'quintanar', 'racing_ferrol', 'rangers', 'rayo_vallecano', 'rb_leipzig', 'real_betis', 'real_madrid', 'real_sociedad', 'red_bull_salzburg', 'rennes', 'rubi', 'sestao', 'sevilla', 'shakhtar_donetsk', 'sparta_prague', 'tardienta', 'tenerife', 'terrassa', 'tudelano', 'turegano', 'ud_logrones', 'union_berlin', 'unionistas_sal', 'valencia', 'valle_egues', 'villanovense', 'villarreal', 'yeclano', 'zamora']

BUNDESLIGA_TEAMS = ['aberdeen', 'arminia', 'arsenal', 'astoria_walldorf', 'atletico_madrid', 'augsburg', 'bayer_leverkusen', 'bayern_munich', 'bochum', 'braga', 'darmstadt_98', 'dortmund', 'eintracht_frankfurt', 'elversberg', 'fc_copenhagen', 'fc_teutonia_ottensen', 'freiburg', 'galatasaray', 'hacken', 'heidenheim', 'hertha_bsc', 'hjk_helsinki', 'hoffenheim', 'homburg', 
'kaiserslautern', 'koln', 'lazio', 'lens', 'levski_sofia', 'lokomotive_leipzig', 'lubeck', 'mainz_05', 'manchester_city', 'manchester_united', 'milan', 'molde', 'monchengladbach', 'napoli', 'newcastle_united', 'olympiacos', 'osnabruck', 'paok', 'paris_saint-germain', 'preussen_munster', 'psv_eindhoven', 'qarabag', 'rb_leipzig', 'real_madrid', 'red_star_belgrade', 'roma', 'rostocker_fc', 'saarbrucken', 'sandhausen', 'stuttgart', 'sv_oberachern', 'tsc_backa_top', 'tsg_balingen', 'tsv_schott_mainz', 'tus_bersenbruck', 'tus_makkabi_berlin', 'union_berlin', 'union_sg', 'unterhaching', 'viktoria_koln', 'wehen_wiesbaden', 'werder_bremen', 'west_ham_united', 'wolfsburg', 'young_boys']


@app.route('/teams', methods=['GET'])
def return_teams():
    return jsonify({
        'teams_availables': {
                'PremierLeague': PREMIERLEAGUE_TEAMS,
                'LaLiga': LALIGA_TEAMS,
                'BundesLiga': BUNDESLIGA_TEAMS,
            },
    })


@app.route('/<team>/<number_games>', methods=['GET'])
def return_team_games_per_number(team, number_games):
    team = str(unidecode(team.strip().lower().replace(' ', '_')))
    number_games = int(number_games)

    if team in PREMIERLEAGUE_TEAMS:
        data = db.get_games_per_team(camp='PremierLeague', team=team, number_games=number_games)
    elif team in LALIGA_TEAMS:
        data = db.get_games_per_team(camp='LaLiga', team=team, number_games=number_games)
    elif team in BUNDESLIGA_TEAMS:
        data = db.get_games_per_team(camp='BundesLiga', team=team, number_games=number_games)
    else:
        data = {
            'error':True,
            'message': 'Time não encontrado',
            'teams_availables': {
                'PremierLeague': PREMIERLEAGUE_TEAMS,
                'LaLiga': LALIGA_TEAMS,
                'BundesLiga': BUNDESLIGA_TEAMS,
            },
        }
        return jsonify(data)

    return jsonify({
        'error': False,
        'data': data
    })


if __name__ == '__main__':
    app.run(debug=True)