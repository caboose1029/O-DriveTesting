# This file contains the ODriveDatabase class, which is used to interact with the ODrive database.
import sqlite3

class ODriveDatabase:
    """
    A class representing a database for storing ODrive data.

    Attributes:
        path (str): The path to the database file.
        
        conn (sqlite3.Connection): The connection to the database.
        
        cursor (sqlite3.Cursor): The cursor for executing SQL queries.

    Methods:
        open_connection(self): Opens a connection to the database.
        
        close_connection(self): Closes the connection to the database.
        
        create_odrive_table(self): Creates the ODriveData table in the database.
        
        insert_odrive_data(self, data): Inserts ODrive data into the database.
        
        get_all_data(self): Retrieves all data from the ODrive Data table.
        
        get_column(self, column, table, trial_id): Retrieves a specific column from a table for a given trial ID.
        
        get_current_odrive_data(self): Retrieves the most recent data from the ODrive Data table.
        
        query_trial(self): Queries the database to determine the latest trial ID.
    """
    def __init__(self, database_path=None):
        """
        Initializes the ODriveDatabase_DB object.

        Args:
            database_path (str, optional): The path to the database file. Defaults to 'odrive.db'.
        """
        if database_path is None:
            self.path = 'odrive.db'
        else:
            self.path = database_path

        self.conn = self.open_connection()
        # self.cursor = self.conn.cursor()
        # self.create_odrive_table()


    def open_connection(self):
        """
        Opens a connection to the database.

        Returns:
            sqlite3.Connection: The connection to the database.
        """
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()

    def close_connection(self):
        """
        Closes the connection to the database.
        """
        self.conn.close()


    def create_odrive_table(self):
        """
        Creates the ODriveData table in the database.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ODriveData (
                UniqueID INTEGER PRIMARY KEY AUTOINCREMENT,                
                run_id INTEGER,
                delta_time REAL,
                position REAL, velocity REAL, torque_target REAL,
                torque_estimate REAL, bus_voltage REAL, bus_current REAL, 
                iq_setpoint REAL, iq_measured REAL, electrical_power REAL, mechanical_power REAL
            )
        ''')
        self.conn.commit()


    def insert_imu_data(self, run_id, dt, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z):
        """
        Inserts IMU data into the database.

        Args:
            run_id (int): The run ID.
            dt (float): The delta time.
            acc_x (float): The accelerometer X-axis value.
            acc_y (float): The accelerometer Y-axis value.
            acc_z (float): The accelerometer Z-axis value.
            gyro_x (float): The gyroscope X-axis value.
            gyro_y (float): The gyroscope Y-axis value.
            gyro_z (float): The gyroscope Z-axis value.
            mag_x (float): The magnetometer X-axis value.
            mag_y (float): The magnetometer Y-axis value.
            mag_z (float): The magnetometer Z-axis value.
        """
        self.cursor.execute('''
                            INSERT INTO imu_data (run_id, delta_time, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                            (run_id, dt, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z))
        self.conn.commit()


    def insert_odrive_data(self, trial_id, time, position, velocity, torque_target, torque_estimate, bus_voltage, bus_current, iq_setpoint, iq_measured, electrical_power, mechanical_power):
        """
        Inserts ODrive data into the database.

        Args:
            run_id (int): The run ID.
            dt (float): The delta time.
            position (float): The position value.
            velocity (float): The velocity value.
            torque_target (float): The torque target value.
            torque_estimate (float): The torque estimate value.
            bus_voltage (float): The bus voltage value.
            bus_current (float): The bus current value.
            iq_setpoint (float): The IQ setpoint value.
            iq_measured (float): The IQ measured value.
            electrical_power (float): The electrical power value.
            mechanical_power (float): The mechanical power value.
        """
        self.cursor.execute('''INSERT INTO odrive_data (trial_id, time, position, velocity, torque_target, torque_estimate, bus_voltage,
                               bus_current, iq_setpoint, iq_measured, electrical_power, mechanical_power) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                             (trial_id, time, position, velocity, torque_target, torque_estimate, bus_voltage,
                               bus_current, iq_setpoint, iq_measured, electrical_power, mechanical_power))
        self.conn.commit()


    def get_all_odrive_data(self):
        """
        Retrieves all data from the IMUData table.

        Returns:
            list: A list of tuples representing the retrieved data.
        """
        self.cursor.execute("SELECT * FROM ODriveData")
        return self.cursor.fetchall()


    def get_column(self, column, table, run):
        """
        Retrieves a specific column from a table for a given run.

        Args:
            column (str): The name of the column to retrieve.
            table (str): The name of the table.
            run (int): The run ID.

        Returns:
            list: A list of tuples representing the retrieved column data.
        """
        query = "SELECT {}, time FROM {} WHERE trial_id = {}".format(column, table, run)
        self.cursor.execute(query)
        column_data = self.cursor.fetchall()
        return column_data


    def get_current_odrive_data(self):
        """
        Retrieves the most recent data from the IMUData table.

        Returns:
            tuple: A tuple representing the most recent data.
        """
        self.conn = sqlite3.connect(self.path)
        self.cursor.execute("SELECT * FROM ODriveData ORDER BY id DESC LIMIT 1")
        return self.cursor.fetchall()


    def query_trial(self):
        """
        Queries the database to determine the latest run ID.

        Returns:
            int: The latest run ID.
        """
        trial_id = None

        self.cursor.execute("SELECT trial_id FROM ODriveData ORDER BY trial_id DESC LIMIT 1")
        trial_id = self.cursor.fetchone()

        if trial_id is None:
            trial_id = 1
        else:
            return trial_id[0] + 1
