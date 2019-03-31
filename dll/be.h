// Header file for use with bee.dll

// unique board type identifiers
#define	BRD_WASP			0x0057
#define BRD_MINIBEE			0x0003
#define BRD_MAXIBEE			0x0058
#define BRD_DIGIBEE			0x0059
#define BRD_MOTORBEE		0x005B
#define BRD_DIGIBEEPLUS		0x005C
#define BRD_STEPPERBEE		0x005D

// error messages returned from function calls
#define	ERRBEE_WRONGTYPE		1			// wrong board type for this command
#define	ERRBEE_INVALID_HANDLE	2			// device write failure due to invalid handle
#define ERRBEE_READTIMEOUT		3			// device failed to respond to a read request

// General Functions
typedef int		(*Type_InitBee)();
typedef int		(*Type_GetBoardType)(int DevNum);

// MiniBee Functions
typedef int		(*Type_MB_SetOutputs)(int DevNum, int Outputs);

// Wasp Functions
typedef int		(*Type_WSP_ReadInputs)(int DevNum, int *Analogue);
typedef int		(*Type_WSP_SetOutputs)(int DevNum, int Outputs);
typedef int		(*Type_WSP_SetSensitivity)(int DevNum, int Sensitivity);

// MaxiBee Functions
typedef int		(*Type_MXB_SetOutputs)(int DevNum, unsigned int Outputs1, unsigned int Outputs2);

// DigiBee Functions
typedef int		(*Type_DGB_ReadInputs)(int DevNum, unsigned int *Inputs);
typedef int		(*Type_DGB_SetOutputs)(int DevNum, unsigned int Outputs);

// DigiBee+ Functions
typedef int		(*Type_DGBP_ReadInputs)(int DevNum, unsigned int *Inputs);
typedef int		(*Type_DGBP_SetOutputs)(int DevNum, unsigned int Outputs);
typedef int		(*Type_DGBP_ReadAnalogueInputs)(int devnum, int *aip1, int *aip2, int *aip3, int *aip4);
typedef int		(*Type_DGBP_SetSensitivity)(int devnum, int sensitivity);

// MotorBee Functions
typedef int		(*Type_MTB_SetMotors)(int DevNum, int on1, int speed1, int on2, int speed2, int on3, int speed3, int on4, int speed4, int servo);
typedef int		(*Type_MTB_Digital_IO)(int DevNum, int *inputs, int outputs);

// StepperBee Functions
typedef int		(*Type_STP_RunMotor1)(int devnum, int steps, int interval, int direction, int outputs);
typedef int		(*Type_STP_StopMotor1)(int devnum, int outputs);
typedef int		(*Type_STP_RunMotor2)(int devnum, int steps, int interval, int direction, int outputs);
typedef int		(*Type_STP_StopMotor2)(int devnum, int outputs);
typedef int		(*Type_STP_SetStepMode)(int devnum, int M1Mode, int M2Mode);
typedef int		(*Type_STP_GetCurrentStatus)(int devnum, int *M1Active, int *M2Active, int *M1Steps, int *M2Steps, int *Inputs);

