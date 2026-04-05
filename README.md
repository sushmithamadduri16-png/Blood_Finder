Here’s a **short, clean, and complete README description** (with future scope included) 👇

---

# 🩸 Smart Blood Donor Finder

A real-time web application built using **Streamlit** that helps users find nearby blood donors based on selected blood groups and distance. It is designed for emergency situations to quickly connect blood seekers with available donors.



## 🚀 Features

* 🔍 Select multiple blood groups (O+, O-, A+, A-, B+, B-, AB+, AB-)
* 📏 Filter donors by distance (km)
* 📍 Location-based matching using Haversine formula
* 🗺️ Map view of nearby donors
* 📡 Ping system (request → accept/decline)
* 📞 Contact details shown only after acceptance
* 🌍 Live GPS tracking (browser-based)



## 🛠️ Tech Stack

* Python, Streamlit, Pandas
* streamlit-js-eval (for geolocation)



## ⚙️ How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```



## ⚠️ Note

* Uses a simulated donor response system
* Requires browser location permission for GPS
* Uses a static dataset (no real database yet)

---

## 🔮 Future Scope

* 🔗 Integration with real-time databases (Firebase/MongoDB)
* 📲 SMS/WhatsApp alerts for donor requests
* 🔐 User authentication for donors and seekers
* 🚑 Emergency auto-alert system
* 📱 Mobile app development

---

##  Purpose

To demonstrate how technology can support real-time blood donation and save lives in emergencies.




