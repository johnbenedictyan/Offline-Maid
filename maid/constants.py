# Imports from python

# Imports from django
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Imports from other apps

# Imports from within the app

# Utiliy Classes and Functions

# Start of Constants

class FullNationsChoices(models.TextChoices):
    AFGHANISTAN	                = 'AFG', _('Afghanistan')
    ALBANIA	                    = 'ALB', _('Albania')
    ALGERIA	                    = 'DZA', _('Algeria')
    AMERICAN_SAMOA	            = 'ASM', _('American Samoa')
    ANDORRA	                    = 'AND', _('Andorra')
    ANGOLA	                    = 'AGO', _('Angola')
    ANGUILLA	                = 'AIA', _('Anguilla')
    ANTARCTICA	                = 'ATA', _('Antarctica')
    ANTIGUA_AND_BARBUDA	        = 'ATG', _('Antigua and Barbuda')
    ARGENTINA	                = 'ARG', _('Argentina')
    ARMENIA	                    = 'ARM', _('Armenia')
    ARUBA	                    = 'ABW', _('Aruba')
    AUSTRALIA	                = 'AUS', _('Australia')
    AUSTRIA	                    = 'AUT', _('Austria')
    AZERBAIJAN	                = 'AZE', _('Azerbaijan')
    BAHAMAS                     = 'BHS', _('Bahamas (the)')
    BAHRAIN	                    = 'BHR', _('Bahrain')
    BANGLADESH	                = 'BGD', _('Bangladesh')
    BARBADOS	                = 'BRB', _('Barbados')
    BELARUS	                    = 'BLR', _('Belarus')
    BELGIUM	                    = 'BEL', _('Belgium')
    BELIZE	                    = 'BLZ', _('Belize')
    BENIN	                    = 'BEN', _('Benin')
    BERMUDA	                    = 'BMU', _('Bermuda')
    BHUTAN	                    = 'BTN', _('Bhutan')
    BOLIVIA	                    = 'BOL', _('Bolivia (Plurinational State of)')
    BONAIRE_SINT_EUSTATIUS_SABA	= 'BES', _('Bonaire, Sint Eustatius and Saba')
    BOSNIA_AND_HERZEGOVINA	    = 'BIH', _('Bosnia and Herzegovina')
    BOTSWANA                    = 'BWA', _('Botswana')
    BOUVET_ISLAND	            = 'BVT', _('Bouvet Island')
    BRAZIL	                    = 'BRA', _('Brazil')
    BRIT_INDIAN_OCEAN_TERRITORY = 'IOT', _('British Indian Ocean Territory')
    BRUNEI_DARUSSALAM	        = 'BRN', _('Brunei Darussalam')
    BULGARIA	                = 'BGR', _('Bulgaria')
    BURKINA_FASO	            = 'BFA', _('Burkina Faso')
    BURUNDI	                    = 'BDI', _('Burundi')
    CABO_VERDE	                = 'CPV', _('Cabo Verde')
    CAMBODIA	                = 'KHM', _('Cambodia')
    CAMEROON	                = 'CMR', _('Cameroon')
    CANADA	                    = 'CAN', _('Canada')
    CAYMAN_ISLANDS	            = 'CYM', _('Cayman Islands (the)')
    CENTRAL_AFRICAN_REPUBLIC    = 'CAF', _('Central African Republic (the)')
    CHAD                        = 'TCD', _('Chad')
    CHILE                       = 'CHL', _('Chile')
    CHINA                       = 'CHN', _('China')
    CHRISTMAS_ISLAND            = 'CXR', _('Christmas Island')
    COCOS_ISLANDS               = 'CCK', _('Cocos (Keeling) Islands (the)')
    COLOMBIA                    = 'COL', _('Colombia')
    COMOROS                     = 'COM', _('Comoros (the)')
    CONGO_DEMOCRATIC_REPUBLIC   = 'COD', _('Congo (the Democratic Republic of)')
    CONGO                       = 'COG', _('Congo (the)')
    COOK_ISLANDS                = 'COK', _('Cook Islands (the)')
    COSTA_RICA                  = 'CRI', _('Costa Rica')
    CROATIA                     = 'HRV', _('Croatia')
    CUBA                        = 'CUB', _('Cuba')
    CURACAO                     = 'CUW', _('Curaçao')
    CYPRUS                      = 'CYP', _('Cyprus')
    CZECHIA                     = 'CZE', _('Czechia')
    COTE_DIVOIRE                = 'CIV', _('Côte d\'Ivoire')
    DENMARK                     = 'DNK', _('Denmark')
    DJIBOUTI                    = 'DJI', _('Djibouti')
    DOMINICA                    = 'DMA', _('Dominica')
    DOMINICAN_REPUBLIC          = 'DOM', _('Dominican Republic (the)')
    ECUADOR                     = 'ECU', _('Ecuador')
    EGYPT                       = 'EGY', _('Egypt')
    EL_SALVADOR                 = 'SLV', _('El Salvador')
    EQUATORIAL_GUINEA           = 'GNQ', _('Equatorial Guinea')
    ERITREA                     = 'ERI', _('Eritrea')
    ESTONIA                     = 'EST', _('Estonia')
    ESWATINI                    = 'SWZ', _('Eswatini')
    ETHIOPIA                    = 'ETH', _('Ethiopia')
    FALKLAND_ISLANDS            = 'FLK', _('Falkland Islands (the) [Malvinas]')
    FAROE_ISLANDS               = 'FRO', _('Faroe Islands (the)')
    FIJI                        = 'FJI', _('Fiji')
    FINLAND                     = 'FIN', _('Finland')
    FRANCE                      = 'FRA', _('France')
    FRENCH_GUIANA               = 'GUF', _('French Guiana')
    FRENCH_POLYNESIA            = 'PYF', _('French Polynesia')
    FRENCH_SOUTHERN_TERRITORIES = 'ATF', _('French Southern Territories (the)')
    GABON                       = 'GAB', _('Gabon')
    GAMBIA                      = 'GMB', _('Gambia (the)')
    GEORGIA                     = 'GEO', _('Georgia')
    GERMANY                     = 'DEU', _('Germany')
    GHANA                       = 'GHA', _('Ghana')
    GIBRALTAR                   = 'GIB', _('Gibraltar')
    GREECE                      = 'GRC', _('Greece')
    GREENLAND                   = 'GRL', _('Greenland')
    GRENADA                     = 'GRD', _('Grenada')
    GUADELOUPE                  = 'GLP', _('Guadeloupe')
    GUAM                        = 'GUM', _('Guam')
    GUATEMALA                   = 'GTM', _('Guatemala')
    GUERNSEY                    = 'GGY', _('Guernsey')
    GUINEA                      = 'GIN', _('Guinea')
    GUINEA_BISSAU               = 'GNB', _('Guinea-Bissau')
    GUYANA                      = 'GUY', _('Guyana')
    HAITI                       = 'HTI', _('Haiti')
    HEARD_AND_MCDONALD_ISLANDS  = 'HMD', _('Heard Island and McDonald Islands')
    HOLY_SEE                    = 'VAT', _('Holy See (the)')
    HONDURAS                    = 'HND', _('Honduras')
    HONG_KONG                   = 'HKG', _('Hong Kong')
    HUNGARY                     = 'HUN', _('Hungary')
    ICELAND                     = 'ISL', _('Iceland')
    INDIA                       = 'IND', _('India')
    INDONESIA                   = 'IDN', _('Indonesia')
    IRAN                        = 'IRN', _('Iran (Islamic Republic of)')
    IRAQ                        = 'IRQ', _('Iraq')
    IRELAND                     = 'IRL', _('Ireland')
    ISLE_OF_MAN                 = 'IMN', _('Isle of Man')
    ISRAEL                      = 'ISR', _('Israel')
    ITALY                       = 'ITA', _('Italy')
    JAMAICA                     = 'JAM', _('Jamaica')
    JAPAN                       = 'JPN', _('Japan')
    JERSEY                      = 'JEY', _('Jersey')
    JORDAN                      = 'JOR', _('Jordan')
    KAZAKHSTAN                  = 'KAZ', _('Kazakhstan')
    KENYA                       = 'KEN', _('Kenya')
    KIRIBATI                    = 'KIR', _('Kiribati')
    NORTH_KOREA                 = 'PRK', _('North Korea')
    SOUTH_KOREA                 = 'KOR', _('South Korea')
    KUWAIT                      = 'KWT', _('Kuwait')
    KYRGYZSTAN                  = 'KGZ', _('Kyrgyzstan')
    LAO                         = 'LAO', _('Lao People\'s Democratic Republic')
    LATVIA                      = 'LVA', _('Latvia')
    LEBANON                     = 'LBN', _('Lebanon')
    LESOTHO                     = 'LSO', _('Lesotho')
    LIBERIA                     = 'LBR', _('Liberia')
    LIBYA                       = 'LBY', _('Libya')
    LIECHTENSTEIN               = 'LIE', _('Liechtenstein')
    LITHUANIA                   = 'LTU', _('Lithuania')
    LUXEMBOURG                  = 'LUX', _('Luxembourg')
    MACAO                       = 'MAC', _('Macao')
    MADAGASCAR                  = 'MDG', _('Madagascar')
    MALAWI                      = 'MWI', _('Malawi')
    MALAYSIA                    = 'MYS', _('Malaysia')
    MALDIVES                    = 'MDV', _('Maldives')
    MALI                        = 'MLI', _('Mali')
    MALTA                       = 'MLT', _('Malta')
    MARSHALL_ISLANDS            = 'MHL', _('Marshall Islands (the)')
    MARTINIQUE                  = 'MTQ', _('Martinique')
    MAURITANIA                  = 'MRT', _('Mauritania')
    MAURITIUS                   = 'MUS', _('Mauritius')
    MAYOTTE	                    = 'MYT', _('Mayotte')
    MEXICO	                    = 'MEX', _('Mexico')
    MICRONESIA                  = 'FSM', _('Micronesia (Federated States of)')
    MOLDOVA	                    = 'MDA', _('Moldova (the Republic of)')
    MONACO                      = 'MCO', _('Monaco')
    MONGOLIA                    = 'MNG', _('Mongolia')
    MONTENEGRO                  = 'MNE', _('Montenegro')
    MONTSERRAT                  = 'MSR', _('Montserrat')
    MOROCCO	                    = 'MAR', _('Morocco')
    MOZAMBIQUE                  = 'MOZ', _('Mozambique')
    MYANMAR	                    = 'MMR', _('Myanmar')
    NAMIBIA	                    = 'NAM', _('Namibia')
    NAURU                       = 'NRU', _('Nauru')
    NEPAL                       = 'NPL', _('Nepal')
    NETHERLANDS                 = 'NLD', _('Netherlands (the)')
    NEW_CALEDONIA               = 'NCL', _('New Caledonia')
    NEW_ZEALAND                 = 'NZL', _('New Zealand')
    NICARAGUA                   = 'NIC', _('Nicaragua')
    NIGER                       = 'NER', _('Niger (the)')
    NIGERIA	                    = 'NGA', _('Nigeria')
    NIUE	                    =  'NIU', _('Niue')
    NORFOLK_ISLAND              = 'NFK', _('Norfolk Island')
    NORTHERN_MARIANA_ISLANDS    = 'MNP', _('Northern Mariana Islands (the)')
    NORWAY	                    = 'NOR', _('Norway')
    OMAN	                    = 'OMN', _('Oman')
    PAKISTAN	                = 'PAK', _('Pakistan')
    PALAU	                    = 'PLW', _('Palau')
    PALESTINE                   = 'PSE', _('Palestine, State of')
    PANAMA	                    = 'PAN', _('Panama')
    PAPUA_NEW_GUINEA            = 'PNG', _('Papua New Guinea')
    PARAGUAY	                = 'PRY', _('Paraguay')
    PERU	                    = 'PER', _('Peru')
    PHILIPPINES	                = 'PHL', _('Philippines (the)')
    PITCAIRN	                = 'PCN', _('Pitcairn')
    POLAND	                    = 'POL', _('Poland')
    PORTUGAL	                = 'PRT', _('Portugal')
    PUERTO_RICO	                = 'PRI', _('Puerto Rico')
    QATAR	                    = 'QAT', _('Qatar')
    NORTH_MACEDONIA	            = 'MKD', _('Republic of North Macedonia')
    ROMANIA	                    = 'ROU', _('Romania')
    RUSSIAN                     = 'RUS', _('Russian Federation (the)')
    RWANDA	                    = 'RWA', _('Rwanda')
    REUNION	                    = 'REU', _('Réunion')
    SAINT_BARTHELEMY	        = 'BLM', _('Saint Barthélemy')
    SAINT_HELENA                = 'SHN', _('Saint Helena, Ascension')
    SAINT_KITTS_AND_NEVIS       = 'KNA', _('Saint Kitts and Nevis')
    SAINT_LUCIA                 = 'LCA', _('Saint Lucia')
    SAINT_MARTIN                = 'MAF', _('Saint Martin (French part)')
    SAINT_PIERRE_AND_MIQUELON   = 'SPM', _('Saint Pierre and Miquelon')
    SAINT_VINCENT               = 'VCT', _('Saint Vincent and the Grenadines')
    SAMOA                       = 'WSM', _('Samoa')
    SAN_MARINO                  = 'SMR', _('San Marino')
    SAO_TOME_AND_PRINCIPE       = 'STP', _('Sao Tome and Principe')
    SAUDI_ARABIA                = 'SAU', _('Saudi Arabia')
    SENEGAL                     = 'SEN', _('Senegal')
    SERBIA                      = 'SRB', _('Serbia')
    SEYCHELLES                  = 'SYC', _('Seychelles')
    SIERRA_LEONE                = 'SLE', _('Sierra Leone')
    SINGAPORE                   = 'SGP', _('Singapore')
    SINT_MAARTEN                = 'SXM', _('Sint Maarten (Dutch part)')
    SLOVAKIA                    = 'SVK', _('Slovakia')
    SLOVENIA                    = 'SVN', _('Slovenia')
    SOLOMON_ISLANDS             = 'SLB', _('Solomon Islands')
    SOMALIA                     = 'SOM', _('Somalia')
    SOUTH_AFRICA                = 'ZAF', _('South Africa')
    SOUTH_GEORGIA               = 'SGS', _('South Georgia')
    SOUTH_SUDAN	                = 'SSD', _('South Sudan')
    SPAIN	                    = 'ESP', _('Spain')
    SRI_LANKA	                = 'LKA', _('Sri Lanka')
    SUDAN	                    = 'SDN', _('Sudan (the)')
    SURINAME	                = 'SUR', _('Suriname')
    SVALBARD_AND_JAN_MAYEN	    = 'SJM', _('Svalbard and Jan Mayen')
    SWEDEN	                    = 'SWE', _('Sweden')
    SWITZERLAND	                = 'CHE', _('Switzerland')
    SYRIAN_ARAB_REPUBLIC	    = 'SYR', _('Syrian Arab Republic')
    TAIWAN 	                    = 'TWN', _('Taiwan')
    TAJIKISTAN	                = 'TJK', _('Tajikistan')
    TANZANIA                    = 'TZA', _('Tanzania, United Republic of')
    THAILAND	                = 'THA', _('Thailand')
    TIMOR_LESTE	                = 'TLS', _('Timor-Leste')
    TOGO	                    = 'TGO', _('Togo')
    TOKELAU	                    = 'TKL', _('Tokelau')
    TONGA	                    = 'TON', _('Tonga')
    TRINIDAD_AND_TOBAGO	        = 'TTO', _('Trinidad and Tobago')
    TUNISIA	                    = 'TUN', _('Tunisia')
    TURKEY	                    = 'TUR', _('Turkey')
    TURKMENISTAN	            = 'TKM', _('Turkmenistan')
    TURKS_AND_CAICOS_ISLANDS	= 'TCA', _('Turks and Caicos Islands (the)')
    TUVALU	                    = 'TUV', _('Tuvalu')
    UGANDA	                    = 'UGA', _('Uganda')
    UKRAINE	                    = 'UKR', _('Ukraine')
    UNITED_ARAB_EMIRATES        = 'ARE', _('United Arab Emirates (the)')
    UNITED_KINGDOM              = 'GBR', _('United Kingdom')
    UNITED_STATES               = 'USA', _('United States of America (the)')
    URUGUAY	                    = 'URY', _('Uruguay')
    UZBEKISTAN	                = 'UZB', _('Uzbekistan')
    VANUATU	                    = 'VUT', _('Vanuatu')
    VENEZUELA                   = 'VEN', _('Venezuela (Bolivarian Republic of)')
    VIETNAM	                    = 'VNM', _('Viet Nam')
    VIRGIN_ISLANDS_BRITISH	    = 'VGB', _('Virgin Islands (British)')
    VIRGIN_ISLANDS_US	        = 'VIR', _('Virgin Islands (U.S.)')
    WALLIS_AND_FUTUNA	        = 'WLF', _('Wallis and Futuna')
    WESTERN_SAHARA	            = 'ESH', _('Western Sahara')
    YEMEN	                    = 'YEM', _('Yemen')
    ZAMBIA	                    = 'ZMB', _('Zambia')
    ZIMBABWE	                = 'ZWE', _('Zimbabwe')
    ALAND_ISLANDS	            = 'ALA', _('Åland Islands')

class MaidCountryOfOrigin(models.TextChoices):
    BANGLADESH  = 'BGD', _('Bangladesh')
    CAMBODIA    = 'KHM', _('Cambodia')
    INDIA       = 'IND', _('India')
    INDONESIA   = 'IDN', _('Indonesia')
    MYANMAR	    = 'MMR', _('Myanmar')
    PHILIPPINES = 'PHL', _('Philippines (the)')
    SRI_LANKA   = 'LKA', _('Sri Lanka')
    OTHERS      = 'OTH', _('Others')

class PreferenceChoices(models.IntegerChoices):
    LEAST_PREFERRED = 1, _('Least preferred')
    LESS_PREFERRED = 2, _('Less preferred')
    NO_PREFERENCE = 3, _('No preference')
    MORE_PREFERRED = 4, _('More preferred')
    MOST_PREFERRED = 5, _('Most preferred')

class MaidCareRemarkChoices(models.TextChoices):
    OWN_COUNTRY = 'OC', _('Experience in own country')
    OVERSEAS = 'OV', _('Experience in overseas')
    SINGAPORE = 'SG', _('Experience in Singapore')
    OWN_COUNTRY_SINGAPORE = 'OC_SG', _(
        'Experience in own country and Singapore'
    )
    OWN_COUNTRY_OVERSEAS = 'OC_O', _('Experience in own country and overseas')
    OWN_COUNTRY_OVERSEAS_SINGPAPORE = 'OC_O_SG', _(
        'Experience in own country, overseas and Singapore'
    )
    NO_EXP = 'NE', _('No experience, but willing to learn')
    NOT_WILLING = 'NW', _('Not willing')
    OTHERS = 'OTH', _('Other remarks (Please specify)')

class TypeOfMaidChoices(models.TextChoices):
    NEW = 'NEW', _('No Experience')
    TRANSFER = 'TRF', _('Transfer')
    SINGAPORE_EXPERIENCE = 'SGE', _('Singapore Experience')
    OVERSEAS_EXPERIENCE = 'OVE', _('Overseas Experience')
        
# The reason why we are not extending any of these classes is due to the fact
# that python does not allow the extending of enumeration type classes
# models.IntegerChoices and models.TextChoices are enumeration type classes