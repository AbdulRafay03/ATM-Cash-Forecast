# Atm Cash Forecasting
Your project appears to focus on **ATM Cash Forecasting** with a user interface that allows manual input of specific features, processes them with a machine learning model, and provides output predictions.

Here’s a comprehensive overview:

### **1. Project Goal:**
The objective of this project is to **predict ATM cash requirements** or trends using a machine learning model. The predictions are based on various factors such as holidays, day of the week, payday sequences, and transactional patterns over specific time periods.

### **2. Core Components:**
- **User Interface (UI):**
  - A graphical interface built using `Tkinter` where users can manually input features related to ATM transactions.
  - Input fields include:
    - `IsHoliday`, `Year`, `Month`, `DayOfWeek`, `Quarter`, etc.
    - Features such as `HolidayType`, `Event`, and others are provided as dropdowns with relevant options.
  - The UI allows users to submit the input values to the machine learning model for inference.
  - A logger window is also embedded in the UI to provide feedback or log operations.

- **Feature Set:**
  - The model uses a comprehensive set of features, including:
    - **Date Features**: `Year`, `Month`, `DayOfWeek`, `DayOfYear`, `Quarter`.
    - **Transaction Trends**: `Last7Days_mean`, `Last30Days_mean`, `Difference`.
    - **Holiday and Event Details**: `IsHoliday`, `HolidayType`, `Event`, `HolidaySequence`.
    - **Categorical Features**: `IsWeekend`, `Paydays`, etc.
  
  These features help the model capture transactional patterns and specific event impacts on ATM usage.

- **Label Encoding:**
  - Categorical features such as `HolidayType`, `Event`, and others are encoded using a `LabelEncoder` to convert them into numeric form before passing them into the model.

- **Model Integration:**
  - Several machine learning models (e.g., `Gradient Boosting`, `XGBoost`, `Random Forest`, `LightGBM`, etc.) are integrated into the project.
  - The system takes the user inputs, encodes them, and then passes them to the `infer` method of the models for predictions.
  - The results are displayed on the UI after the inference.

### **3. Key Features of the Application:**
- **Manual Input & Model Prediction:**
  Users can input specific values such as holiday sequences, payday details, transaction trends, etc., which are crucial for predicting ATM cash needs.
  
- **Model Inference & Results Display:**
  The results from the models (cash predictions) are displayed dynamically on the UI after input submission.

### **4. Technologies Used:**
- **Python Libraries:**
  - **Tkinter**: Used for creating the graphical interface.
  - **Scikit-learn**: Used for machine learning (label encoding, modeling, etc.).
  - **PyInstaller**: For packaging the Python script into a standalone executable.

- **Machine Learning Models:**
  - Various models like **Gradient Boosting**, **LightGBM**, **CatBoost**, **XGBoost**, **Random Forest**, and potentially **Stacking Regressor** are used for predictions.
  
### **5. Workflow:**
1. **User Inputs**: The user provides input values through the UI fields, which include both numeric and categorical data.
2. **Feature Encoding**: Categorical features are label-encoded using pre-saved encoders.
3. **Model Inference**: The encoded data is passed to a machine learning model for cash flow prediction.
4. **Result Display**: The prediction results (likely ATM cash forecast) are displayed on the UI.
5. **Executable File**: The final Python script can be converted into a standalone `.exe` file using `PyInstaller`, making it easy to distribute the application without requiring Python installation.

### **6. Challenges Solved:**
- **Handling Complex Features**: Features such as holidays, weekends, and event sequences play a significant role in ATM transactions. The project efficiently captures these through a combination of dropdowns and automated label encoding.
- **User-Friendly Interface**: The graphical interface allows non-technical users to interact with the machine learning model and get predictions without diving into code.
- **Predictive Modeling**: The use of multiple machine learning models ensures robust cash flow forecasting, and the combination of various models can potentially improve prediction accuracy.

### **7. Future Improvements:**
- **Enhance Model Accuracy**: Fine-tuning and hyperparameter optimization for the different models can further improve performance.
- **Additional Features**: More features such as weather patterns, geographic location of the ATM, or broader economic indicators could be incorporated to refine predictions.
- **Automated Data Handling**: Instead of manual input, real-time ATM data could be automatically fed into the system, enhancing usability.

In summary, the project combines machine learning with a user-friendly UI to solve a real-world problem of predicting ATM cash needs, using sophisticated feature engineering and model integration.

## Results

| Model           | MSE          | MAE          | MAPE     | R²        |
|-----------------|--------------|--------------|----------|-----------|
| Gradient Boost  | 7706.754390   | 70.036785     | 0.450142 | 0.242991  |
| LightGBM        | 7958.092438   | 71.360411     | 0.460409 | 0.218303  |
| CatBoost        | 7493.748586   | 69.045935     | 0.447735 | 0.263914  |
| Random Forest   | 8032.624521   | 71.478044     | 0.460541 | 0.210982  |
| XGBoost         | 7624.443946   | 69.895835     | 0.451133 | 0.251076  |
| Stacked Reg     | 7616.763010   | 69.839697     | 0.453305 | 0.251831  |
| Average         | 7653.172050   | 69.994031     | 0.452448 | 0.248254  |
| Max             | 7897.089496   | 71.107252     | 0.482975 | 0.224295  |


![Screenshot 2024-07-25 193903](https://github.com/user-attachments/assets/1881b00e-5f01-4804-b12f-7f07fd1f4468)
![Screenshot 2024-07-25 193855](https://github.com/user-attachments/assets/aa73c24a-81c5-43d8-a6e5-94fb9f3c27fb)
![Screenshot 2024-07-25 193933](https://github.com/user-attachments/assets/5feffdfc-bb30-4c0e-8723-8cdbbd996095)
![Screenshot 2024-07-25 193929](https://github.com/user-attachments/assets/9636dfa1-8dbb-44e2-86b4-da300cf9f794)
![Screenshot 2024-07-25 193925](https://github.com/user-attachments/assets/c574cebf-fa0d-4063-9d0d-f1bb97740f29)
![Screenshot 2024-07-25 193915](https://github.com/user-attachments/assets/ac284063-436b-4e72-ad98-07d0a1553384)
![Screenshot 2024-07-25 193909](https://github.com/user-attachments/assets/2930b1ac-d24f-4927-aed0-5c883ac2ea16)
![output](https://github.com/user-attachments/assets/91a4278a-7037-4d0c-bf9f-7407a1b51bd6)
![ss](https://github.com/user-attachments/assets/3d403db3-dde7-44ff-8efe-8a872c117e01)



- USD conversion rates : https://www.investing.com/currencies/usd-pkr-historical-data
