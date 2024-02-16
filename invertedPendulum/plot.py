import matplotlib.pyplot as plt
import odrivedatabaseV2 as db 

class PlotBuild:
    
        def __init__(self, plotname : str, run, columns):
            self.plot = {"plot" : plotname, "columns" : {}}
            self.columns = columns
            self.run = str(run)
            self.unpack_columns()

        def unpack_columns(self):
            encoderData = ["angle"]
            
            ODriveData = ["position", "velocity", "torque_target",
                        "torque_estimate", "bus_voltage", "bus_current", 
                        "iq_setpoint", "iq_measured", "electrical_power", 
                        "mechanical_power"]
            data = []

            for column in self.columns:
                if column in encoderData:
                    column_data = database.get_column(column, "encoderData", self.run) 
                    data.append(column_data)

                elif column in ODriveData:
                    column_data = database.get_column(column, "ODriveData", self.run)
                    data.append(column_data)
                else:
                    print("Column not found in database. Please check the column name and try again.")
                    return

            self.plot_columns(data)

        def plot_columns(self, data):
            # print(data)
            for column_data in data:
                y, x = zip(*column_data)
                plt.plot(x, y)
            plt.legend(self.columns)
            plt.xlabel("Time (s)")
            plt.show()




database = db.ODriveDatabase("invertedPendulum/odrive_data_ip.db")
database.open_connection()
plot1 = PlotBuild("plot1", 1, ["position"])
database.close_connection()


