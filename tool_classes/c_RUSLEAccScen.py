import arcpy
import configuration
import os
from LUCI_SEEA.lib.refresh_modules import refresh_modules

class RUSLEAccScen(object):

    class ToolValidator:
        """Class for validating a tool's parameter values and controlling the behavior of the tool's dialog."""
    
        def __init__(self, parameters):
            """Setup the Geoprocessor and the list of tool parameters."""
            self.params = parameters
    
        def initializeParameters(self):
            """Refine the properties of a tool's parameters.
            This method is called when the tool is opened."""
            return
        
        def updateParameters(self):
            """Modify the values and properties of parameters before internal validation is performed.
            This method is called whenever a parameter has been changed."""
            return
    
        def updateMessages(self):
            """Modify the messages created by internal validation for each tool parameter.
            This method is called after internal validation."""

            import LUCI_SEEA.lib.input_validation as input_validation
            refresh_modules(input_validation)
            
            input_validation.checkFilePaths(self)
    
    def __init__(self):
        self.label = u'Calculate soil loss accounts using two scenario folders'
        self.canRunInBackground = False
        self.category = '3 RUSLE tools'

    def getParameterInfo(self):

        params = []

        # 0 Output__Success
        param = arcpy.Parameter()
        param.name = u'Output__Success'
        param.displayName = u'Output: Success'
        param.parameterType = 'Derived'
        param.direction = 'Output'
        param.datatype = u'Boolean'
        params.append(param)

        # 1 Run_system_checks
        param = arcpy.Parameter()
        param.name = u'Run_system_checks'
        param.displayName = u'Run_system_checks'
        param.parameterType = 'Derived'
        param.direction = 'Output'
        param.datatype = u'Boolean'
        param.value = u'True'
        params.append(param)        

        # 2 Output_Layer_Soil_Loss_Year_A
        param = arcpy.Parameter()
        param.name = u'Output_Layer_Soil_Loss_Year_A'
        param.displayName = u'Soil loss (tons/ha/yr) for year A'
        param.parameterType = 'Derived'
        param.direction = 'Output'
        param.datatype = u'Raster Layer'
        param.symbology = os.path.join(configuration.displayPath, "soillossA.lyr")
        params.append(param)

        # 3 Output_Layer_Soil_Loss_Year_B
        param = arcpy.Parameter()
        param.name = u'Output_Layer_Soil_Loss_Year_B'
        param.displayName = u'Soil loss (tons/ha/yr) for year B'
        param.parameterType = 'Derived'
        param.direction = 'Output'
        param.datatype = u'Raster Layer'
        param.symbology = os.path.join(configuration.displayPath, "soillossB.lyr")
        params.append(param)

        # 4 Output_Difference
        param = arcpy.Parameter()
        param.name = u'Output_Difference'
        param.displayName = u'Difference layer'
        param.parameterType = 'Derived'
        param.direction = 'Output'
        param.datatype = u'Raster Layer'
        param.symbology = os.path.join(configuration.displayPath, "soilloss_diff.lyr")
        params.append(param)

        # 5 Output_folder
        param = arcpy.Parameter()
        param.name = u'Output_folder'
        param.displayName = u'Output folder'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Folder'
        params.append(param)

        # 6 YearA_ScenarioFolder
        param = arcpy.Parameter()
        param.name = u'YearA_ScenarioFolder'
        param.displayName = u'Year A: Scenario folder'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Folder'
        params.append(param)

        # 7 YearB_ScenarioFolder
        param = arcpy.Parameter()
        param.name = u'YearB_ScenarioFolder'
        param.displayName = u'Year B: Scenario folder'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Folder'
        params.append(param)

        # 8 LS-factor option
        param = arcpy.Parameter()
        param.name = u'LS_option'
        param.displayName = u'LS-factor: Method option'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'String'
        param.value = u'Calculate based on slope and length only'
        param.filter.list = [u'Calculate based on slope and length only', u'Include upslope contributing area']
        params.append(param)

        # 9 LSfactor: cutoff slope angle
        param = arcpy.Parameter()
        param.name = u'LSfactor_cutoff_angle'
        param.displayName = u'LS-factor: Cutoff slope angle (degrees)'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Double'
        param.value = u'26.6'
        params.append(param)

        # 10 Rainfall erosivity
        param = arcpy.Parameter()
        param.name = u'Rainfall_erosivity_A'
        param.displayName = u'R-factor for Year A: Rainfall erosivity dataset'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Raster Layer'
        params.append(param)

        # 11 Rainfall erosivity
        param = arcpy.Parameter()
        param.name = u'Rainfall_erosivity_B'
        param.displayName = u'R-factor for Year B: Rainfall erosivity dataset'
        param.parameterType = 'Required'
        param.direction = 'Input'
        param.datatype = u'Raster Layer'
        params.append(param)

        # 12 Pfactor_dataset_A
        param = arcpy.Parameter()
        param.name = u'Pfactor_dataset_A'
        param.displayName = u'P-factor for Year A: Support practice dataset'
        param.parameterType = 'Optional'
        param.direction = 'Input'
        param.datatype = 'Raster Layer'
        params.append(param)

        # 13 Pfactor_dataset_B
        param = arcpy.Parameter()
        param.name = u'Pfactor_dataset_B'
        param.displayName = u'P-factor for Year B: Support practice dataset'
        param.parameterType = 'Optional'
        param.direction = 'Input'
        param.datatype = 'Raster Layer'
        params.append(param)

        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
             return validator(parameters).updateParameters()

    def updateMessages(self, parameters):
        validator = getattr(self, 'ToolValidator', None)
        if validator:
             return validator(parameters).updateMessages()

    def execute(self, parameters, messages):

        import LUCI_SEEA.tools.t_RUSLE_scen_acc as t_RUSLE_scen_acc
        refresh_modules(t_RUSLE_scen_acc)

        t_RUSLE_scen_acc.function(parameters)
