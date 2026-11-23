import matplotlib.pyplot as plt
import streamlit as st
import subprocess
import sys
import json
import pandas as pd

st.set_page_config(
    page_title="UP RENT",
    page_icon="🚚",
    layout="wide"
)

st.title("🚚 UP RENT – Smart Logistics Planner")
st.write("Optimizacija prijevoza radnih strojeva")


# Pregled ulaznih podataka
st.header("📋 Ulazni podaci")

# Primjerni podaci
primjer_kamioni = pd.DataFrame({
    "Kamion": ["Kamion A", "Kamion B"],
    "Nosivost (kg)": [3500, 10000],
    "Maks. strojeva": [2, 3]
})

primjer_strojevi = pd.DataFrame({
    "Stroj": [f"M{i:02d}" for i in range(1, 11)],
    "Težina (kg)": [
        800, 1300, 1800, 2400, 3100,
        3900, 4800, 6100, 7500, 9400
    ]
})

primjer_lokacije = pd.DataFrame({
    "Lokacija": [f"L{i}" for i in range(10)],
    "X": [0, 3, 10, 17, 9, 26, -7, 20, 23, -8],
    "Y": [0, 8, 11, 9, -6, 3, 13, -8, 15, -5]
})

primjer_nalozi = pd.DataFrame({
    "Nalog": [f"N{i:02d}" for i in range(1, 11)],
    "Stroj": [f"M{i:02d}" for i in range(1, 11)],
    "Preuzimanje": [
        "L1", "L2", "L9", "L3", "L0",
        "L5", "L8", "L4", "L6", "L7"
    ],
    "Isporuka": [
        "L3", "L5", "L4", "L0", "L8",
        "L7", "L2", "L9", "L1", "L3"
    ]
})

# Na početku su sve tablice prazne
if "kamioni" not in st.session_state:
    st.session_state.kamioni = primjer_kamioni.iloc[0:0].copy()

if "strojevi" not in st.session_state:
    st.session_state.strojevi = primjer_strojevi.iloc[0:0].copy()

if "lokacije" not in st.session_state:
    st.session_state.lokacije = primjer_lokacije.iloc[0:0].copy()

if "nalozi" not in st.session_state:
    st.session_state.nalozi = primjer_nalozi.iloc[0:0].copy()

# Gumb za učitavanje primjernih podataka
if st.button("📥 Učitaj primjerne podatke"):
    st.session_state.kamioni = primjer_kamioni.copy()
    st.session_state.strojevi = primjer_strojevi.copy()
    st.session_state.lokacije = primjer_lokacije.copy()
    st.session_state.nalozi = primjer_nalozi.copy()
    st.rerun()

if st.button("🧪 Test 1 – Nedovoljna nosivost"):
    st.session_state.kamioni = primjer_kamioni.copy()
    st.session_state.kamioni.loc[
        st.session_state.kamioni["Kamion"] == "Kamion B",
        "Nosivost (kg)"
    ] = 1000

    st.session_state.strojevi = primjer_strojevi.copy()
    st.session_state.lokacije = primjer_lokacije.copy()
    st.session_state.nalozi = primjer_nalozi.copy()

    st.rerun()

if st.button("🧪 Test 2 – Prekoračenje radnog vremena"):
    st.session_state.kamioni = primjer_kamioni.copy()
    st.session_state.strojevi = primjer_strojevi.copy()
    st.session_state.lokacije = primjer_lokacije.copy()
    st.session_state.nalozi = primjer_nalozi.copy()

    # L7 pomičemo na 600 km od baze
    st.session_state.lokacije.loc[
        st.session_state.lokacije["Lokacija"] == "L7",
        ["X", "Y"]
    ] = [600, 0]

    st.rerun()

if st.button("🧪 Test 3 – Nepostojeća lokacija"):
    st.session_state.kamioni = primjer_kamioni.copy()
    st.session_state.strojevi = primjer_strojevi.copy()
    st.session_state.lokacije = primjer_lokacije.copy()
    st.session_state.nalozi = primjer_nalozi.copy()

    # N01 pokušava preuzeti stroj na nepostojećoj lokaciji
    st.session_state.nalozi.loc[
        st.session_state.nalozi["Nalog"] == "N01",
        "Preuzimanje"
    ] = "L99"

    st.rerun()

# Prikaz i uređivanje tablica

with st.expander("🚚 Vozni park", expanded=True):
    st.session_state.kamioni = st.data_editor(
        st.session_state.kamioni,
        num_rows="dynamic",
        hide_index=True,
        width="stretch",
        key="editor_kamioni"
    )

with st.expander("🏗️ Strojevi", expanded=True):
    st.session_state.strojevi = st.data_editor(
        st.session_state.strojevi,
        num_rows="dynamic",
        hide_index=True,
        width="stretch",
        key="editor_strojevi"
    )

with st.expander("📍 Lokacije", expanded=True):
    st.session_state.lokacije = st.data_editor(
        st.session_state.lokacije,
        num_rows="dynamic",
        hide_index=True,
        width="stretch",
        key="editor_lokacije"
    )

with st.expander("📦 Transportni nalozi", expanded=True):
    st.session_state.nalozi = st.data_editor(
        st.session_state.nalozi,
        num_rows="dynamic",
        hide_index=True,
        width="stretch",
        key="editor_nalozi"
    )

################################################


if st.button("Optimiziraj rute", type="primary"):
    if any(st.session_state[naziv].empty for naziv in
           ["kamioni", "strojevi", "lokacije", "nalozi"]):
        st.warning("⚠️ Nema dovoljno podataka. Unesite podatke ili kliknite 'Učitaj primjerne podatke' prije optimizacije.")
        st.stop()

    
    with st.spinner("Optimizacija u tijeku..."):
        ulazni_podaci = {
            "trucks": st.session_state.kamioni.to_dict(orient="records"),
            "machines": st.session_state.strojevi.to_dict(orient="records"),
            "locations": st.session_state.lokacije.to_dict(orient="records"),
            "orders": st.session_state.nalozi.to_dict(orient="records")
        }

    
    
    

        result = subprocess.run(
            [sys.executable, "optimizer.py"],
            input=json.dumps(ulazni_podaci),
            capture_output=True,
            text=True,
            timeout=25
        )

    if result.returncode != 0:
        greska = result.stderr.strip().splitlines()
        poruka = greska[-1] if greska else "Nepoznata greška."

        if poruka.startswith("ValueError:"):
            st.warning("⚠️ " + poruka.removeprefix("ValueError:").strip())
        else:
            st.error("Dogodila se neočekivana greška tijekom optimizacije.")
            st.code(result.stderr)

    else:
        json_line = next(
            (
                line for line in result.stdout.splitlines()
                if line.startswith("RESULT_JSON:")
            ),
            None
        )

        if json_line is None:
            st.error("Algoritam nije vratio rezultate.")

        else:
            data = json.loads(
                json_line.removeprefix("RESULT_JSON:")
            )

            if not data["success"]:
                st.warning(data["message"])

            else:
                st.success("Optimizacija završena!")

                st.metric(
                    "Ukupna kilometraža",
                    f"{data['total_km']:.1f} km"
                )

                for truck in data["trucks"]:
                    st.subheader(truck["name"])

                    # Izračun vremena
                    vrijeme_voznje_min = round(truck["km"] / 60 * 60)
                    vrijeme_utovara_min = truck["orders"] * 2 * 20
                    ukupno_min = vrijeme_voznje_min + vrijeme_utovara_min

                    col1, col2, col3, col4 = st.columns(4)

                    col1.metric(
                        "Kilometraža",
                        f"{truck['km']:.1f} km"
                    )

                    col2.metric(
                        "Izvršeni nalozi",
                        truck["orders"]
                    )

                    col3.metric(
                        "Vrijeme vožnje",
                        f"{vrijeme_voznje_min // 60} h {vrijeme_voznje_min % 60} min"
                    )

                    col4.metric(
                        "Ukupno radno vrijeme",
                        f"{ukupno_min // 60} h {ukupno_min % 60} min"
                    )


# Grafički prikaz ruta
if "data" in locals() and data.get("success"):

    fig, ax = plt.subplots(figsize=(12, 7))
    colors = ["blue", "red", "green", "orange", "purple", "brown"]
    
    st.subheader("🚚 Redoslijed obilaska lokacija")

    for i, truck in enumerate(data["trucks"]):
        color = colors[i % len(colors)]

        st.markdown(
            f"**:{color}[{truck['name']}]** — "
            f"{truck['orders']} naloga, "
            f"{truck['km']:.1f} km"
        )

        st.write("Ruta: " + " → ".join(truck["route"]))
    st.header("🗺️ Grafički prikaz ruta")
    fig, ax = plt.subplots(figsize=(12, 7))    

    # Koordinate lokacija
    coords = {
        str(row["Lokacija"]): (float(row["X"]), float(row["Y"]))
        for _, row in st.session_state.lokacije.iterrows()
    }

    # Prikaz lokacija
    for name, (x, y) in coords.items():
        ax.scatter(x, y, color="black", s=50, zorder=3)
        ax.text(x + 0.5, y + 0.5, name)

    # Prikaz ruta
    for i, truck in enumerate(data["trucks"]):
        route = truck["route"]

        if len(route) <= 2:
            continue

        color = colors[i % len(colors)]
        segment_number = 0

        for j in range(len(route) - 1):
            start = coords[route[j]]
            end = coords[route[j + 1]]

            if start == end:
                continue

            segment_number += 1

            ax.annotate(
                "",
                xy=end,
                xytext=start,
                arrowprops=dict(
                    arrowstyle="->",
                    color=color,
                    lw=2
                )
            )

            mid_x = (start[0] + end[0]) / 2
            mid_y = (start[1] + end[1]) / 2

            ax.text(
                mid_x, mid_y,
                str(segment_number),
                color="white",
                fontsize=9,
                ha="center",
                va="center",
                bbox=dict(
                    facecolor=color,
                    boxstyle="circle,pad=0.3"
                )
            )

        ax.plot([], [], color=color, label=truck["name"])

    ax.set_title("UP RENT – Optimizirane rute")
    ax.set_xlabel("X (km)")
    ax.set_ylabel("Y (km)")
    ax.grid(True, alpha=0.3)
    ax.axis("equal")
    ax.legend()

    st.pyplot(fig)
    plt.close(fig)
