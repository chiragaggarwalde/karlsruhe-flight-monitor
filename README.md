# ✈️ Karlsruhe Flight Monitor

A simple and interactive **flight tracking dashboard** that shows live aircraft activity over the Karlsruhe region using real-world aviation data.

---

## 🚀 Features

* 📡 Fetches **real-time flight data** from OpenSky API
* 📍 Displays flights on an **interactive map**
* 📊 Shows key metrics:

  * Total flights
  * Countries
  * Highest altitude
  * Average speed
* 🔎 Filter flights by:

  * Country
  * Callsign
* 📈 Visual insights:

  * Top countries
  * Altitude distribution
  * Highest altitude flight
* 💾 Export filtered data as **CSV**

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit** (UI dashboard)
* **Pandas** (data processing)
* **Requests** (API calls)

---

## 📦 Project Structure

```
karlsruhe-flight-monitor/
│
├── app/
│   ├── dashboard.py       # Streamlit app
│   ├── fetch_flights.py   # Data fetching & processing
│
├── data/
│   └── processed/
│       └── flights.csv
│
├── docs/                  # Notes & planning (optional)
├── README.md
└── .gitignore
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```
git clone https://github.com/your-username/karlsruhe-flight-monitor.git
cd karlsruhe-flight-monitor
```

### 2. Create virtual environment

```
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

## ▶️ Run the App

```
streamlit run app/dashboard.py
```

Then open the local URL shown in your terminal.

---

## 🌍 Data Source

* Uses the **OpenSky Network API**
* Provides real-time aircraft position data
* Best coverage in Europe and the US

---

## 📌 Future Improvements

* 🔄 Auto-refresh with adjustable interval
* 🛫 Airport-specific filtering
* 📍 Flight path tracking
* 🔔 Alerts for low altitude / landing aircraft

---

## 📸 Screenshot

*(Add a screenshot of your dashboard here for better presentation)*

---

## 🙌 Acknowledgements

* OpenSky Network for providing free aviation data
* Streamlit for simple and powerful UI development

---

## 📄 License

This project is for educational and portfolio purposes.
