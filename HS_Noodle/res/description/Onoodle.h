#ifndef _Onoodle_H_
#define _Onoodle_H_

enum
{
	NOODLE_GROUP_TITLE			= 10000,
	NOODLE_GROUP_KNOT_PROPS		= 10001,
	NOODLE_GROUP_SPLINE_PROPS	= 10002,

	NOODLE_TYPE					= 110000,
	NOODLE_TYPE_TORUS_A			= 111000,
	NOODLE_TYPE_TORUS_B			= 112000,
	NOODLE_TYPE_TORUS_C			= 113000,

	NOODLE_PRESET_A_KNOT_23		= 111100,
	NOODLE_PRESET_A_KNOT_32		= 111101,
	NOODLE_PRESET_A_KNOT_37		= 111102,
	NOODLE_PRESET_A_KNOT_94		= 111103,

	NOODLE_PRESET_B_STAR_A		= 112100,
	NOODLE_PRESET_B_STAR_B		= 112101,
	NOODLE_PRESET_B_STAR_C		= 112102,
	NOODLE_PRESET_B_STAR_D		= 112103,
	NOODLE_PRESET_B_STAR_E		= 112104,
	NOODLE_PRESET_B_FIG8_A		= 112105,
	NOODLE_PRESET_B_FIG8_B		= 112106,
	NOODLE_PRESET_B_FIG8_C		= 112107,
	NOODLE_PRESET_B_CIRC_A		= 112108,
	NOODLE_PRESET_B_CIRC_B		= 112109,
	NOODLE_PRESET_B_CIRC_C		= 112110,
	NOODLE_PRESET_B_PAIR_A		= 112111,
	NOODLE_PRESET_B_PAIR_B		= 112112,
	NOODLE_PRESET_B_COMP_A		= 112113,
	NOODLE_PRESET_B_COMP_B		= 112114,

	NOODLE_PRESET_C_FLEUR_A		= 113100,
	NOODLE_PRESET_C_FLEUR_B		= 113101,
	NOODLE_PRESET_C_FLEUR_C		= 113102,
	NOODLE_PRESET_C_STAR_A		= 113103,
	NOODLE_PRESET_C_STAR_B		= 113104,
	NOODLE_PRESET_C_STAR_C		= 113105,
	NOODLE_PRESET_C_STAR_D		= 113106,

	NOODLE_POINT_COUNT			= 100101,
	NOODLE_SIZE					= 100102,
	NOODLE_PRESETS				= 100103,
	NOODLE_CUSTOM_PRESET		= 100104,
	NOODLE_FORMULA_VIEW			= 100105,
	NOODLE_FORMULA_SHOW_VALUES	= 100106,

	NOODLE_VAR_P				= 100200,
	NOODLE_VAR_Q				= 100201,
	NOODLE_VAR_M				= 100202,
	NOODLE_VAR_N				= 100203,
	NOODLE_VAR_R				= 100204,
	NOODLE_VAR_S				= 100205,
	NOODLE_SIGN_CHANGE			= 100206,
	NOODLE_INTERLACING			= 100207,
	NOODLE_AUTO_SOLVE			= 100208,

	NOODLE_SPLINE_TYPE			= 11000,
	NOODLE_SPLINE_TYPE_LINEAR	= 11001,
	NOODLE_SPLINE_TYPE_CUBIC	= 11002,
	NOODLE_SPLINE_TYPE_AKIMA	= 11003,
	NOODLE_SPLINE_TYPE_BSPLINE	= 11004,
	NOODLE_SPLINE_TYPE_BEZIER	= 11005,
	NOODLE_SPLINE_CLOSED		= 11100
};

#endif