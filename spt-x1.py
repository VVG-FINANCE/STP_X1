# =========================
# STP-X1 Global Pro - Painéis Flutuantes
# =========================

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

# =========================
# Dados de Mercado
# =========================
market_data = pd.DataFrame({
    "Date": pd.date_range(start="2026-01-01", periods=100, freq='D'),
    "Open": np.random.rand(100)*100 + 100,
    "High": np.random.rand(100)*100 + 110,
    "Low": np.random.rand(100)*100 + 90,
    "Close": np.random.rand(100)*100 + 100
})

market_metrics = {"Momentum": 85, "WaveScaling": 88, "Surf": 90, "RSI": 65, "MACD": 1.5}

# =========================
# Planos de Usuário
# =========================
user_plans = pd.DataFrame({
    "PlanName": ["Gratuito","Básico","Avançado","Completo","Premium"],
    "DailyTradeLimit": [5,10,20,50,100],
    "AccessLevel": ["Básico","Básico","Avançado","Completo","Premium"],
    "TradeFeePercent": [0,0.5,0.3,0.2,0.1]
})

demo_accounts = {t: {"balance":100000,"trades":[]} for t in ["Scalper","DayTrader","SwingTrader","PositionTrader"]}
real_accounts = {}

# =========================
# Advisor (Conselheiro)
# =========================
class Advisor:
    def __init__(self):
        self.alerts = []
    def send_alert(self,msg):
        self.alerts.append({"time":datetime.now(),"message":msg})

advisor = Advisor()

# =========================
# Motor de Trading
# =========================
class TradingEngine:
    def start_trade(self,account,amount,signal,sl,tp1,tp2,tp3,safety_zone,wave_threshold,real=False):
        trade = {
            "amount":amount,
            "signal":signal,
            "sl":sl,
            "tp1":tp1,
            "tp2":tp2,
            "tp3":tp3,
            "safety_zone":safety_zone,
            "wave_threshold":wave_threshold,
            "real":real,
            "timestamp":datetime.now(),
            "status":"Ativo"
        }
        account["trades"].append(trade)
        advisor.send_alert(f"Trade iniciado ({signal}) - Valor: {amount}")
        return trade

    def stop_trade(self,account,trade):
        if trade in account["trades"]:
            trade["status"] = "Interrompido"
            advisor.send_alert(f"Trade interrompido - Valor: {trade['amount']}")

trading_engine = TradingEngine()

# =========================
# Monte Carlo
# =========================
def execute_montecarlo_trade(account, amount, sl, tp1, tp2, tp3, safety_zone):
    outcomes = np.random.normal(loc=1.02, scale=0.03, size=100)
    trades = [amount*o for o in outcomes]
    advisor.send_alert(f"Monte Carlo simulado para {amount} - Média: {np.mean(trades):.2f}")
    return {"TradesSimulados": trades, "MédiaLucro": np.mean(trades)}

# =========================
# Sidebar - Navegação
# =========================
st.sidebar.markdown("## STP-X1 Global Pro")
usuario_plano = st.sidebar.selectbox("Plano do Usuário", user_plans["PlanName"])
pl = user_plans[user_plans["PlanName"] == usuario_plano].iloc[0]
menu = st.sidebar.radio("Menu", ["Dashboard","Charts","Simulators","Reports","Apps","Account Settings"])

# =========================
# DASHBOARD FLUTUANTE
# =========================
if menu=="Dashboard":
    st.header(f"Painel STP-X1 Global Pro - Plano: {usuario_plano}")
    col1,col2,col3 = st.columns([2,2,1])
    with col1:
        st.subheader("Métricas do Mercado")
        st.write(market_metrics)
    with col2:
        st.subheader("Trades Ativos (Flutuante)")
        for acc_name, acc in demo_accounts.items():
            for t in acc["trades"]:
                st.write(f"{acc_name} - {t['signal']} - {t['amount']} - Status: {t['status']}")
    with col3:
        st.subheader("Alertas do Advisor")
        for alert in advisor.alerts[-5:]:
            st.info(f"[{alert['time'].strftime('%H:%M:%S')}] {alert['message']}")

# =========================
# GRÁFICOS INTERATIVOS
# =========================
elif menu=="Charts":
    st.header("Gráficos Interativos e Painéis Flutuantes")
    timeframe = st.selectbox("Timeframe", ["1D","1H","15m"])
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=market_data["Date"], 
        open=market_data["Open"],
        high=market_data["High"],
        low=market_data["Low"],
        close=market_data["Close"], 
        name="Candles"
    ))
    if pl['AccessLevel'] in ["Avançado","Completo","Premium"]:
        fig.add_trace(go.Scatter(x=market_data["Date"], y=market_data["Close"].rolling(10).mean(), line=dict(color='blue',width=1), name="MA10"))
        fig.add_trace(go.Scatter(x=market_data["Date"], y=market_data["Close"].rolling(20).mean(), line=dict(color='orange',width=1), name="MA20"))
        fig.add_trace(go.Scatter(x=market_data["Date"], y=market_data["Close"].rolling(50).mean(), line=dict(color='purple',width=1), name="MA50"))
        fig.add_trace(go.Scatter(x=market_data["Date"], y=np.random.rand(len(market_data))*100+100, line=dict(color='red',width=1), name="RSI"))
    st.plotly_chart(fig,use_container_width=True)

# =========================
# SIMULADORES DOCKABLE
# =========================
elif menu=="Simulators":
    st.header("Simuladores Flutuantes e Modo Automático")
    trader_type = st.selectbox("Tipo de Trader", list(demo_accounts.keys()))
    account_type = st.radio("Conta", ["Demo","Real"])
    account = demo_accounts[trader_type] if account_type=="Demo" else real_accounts.get(trader_type,demo_accounts[trader_type])
    trade_amount = st.number_input("Valor Operação",1,100000,1000)
    auto_mode = st.checkbox("Modo Automático")
    sl = st.number_input("Stop Loss",1,1000,50)
    tp1 = st.number_input("Take Profit 1",1,1000,105)
    tp2 = st.number_input("Take Profit 2",1,1000,110)
    tp3 = st.number_input("Take Profit 3",1,1000,120)
    safety_zone = st.number_input("Safety Zone",1,1000,45)

    col1,col2,col3 = st.columns(3)
    with col1:
        if st.button("Iniciar Operação"):
            if auto_mode:
                mc_summary = execute_montecarlo_trade(account, trade_amount, sl, tp1, tp2, tp3, safety_zone)
                st.subheader("Resumo Monte Carlo")
                st.write(mc_summary)
            else:
                trading_engine.start_trade(account, trade_amount, "Manual Signal", sl, tp1, tp2, tp3, safety_zone,85,False)
                st.success("Operação manual iniciada")
    with col2:
        if st.button("Interromper Última Operação"):
            if account["trades"]:
                trading_engine.stop_trade(account, account["trades"][-1])
            else:
                st.info("Nenhuma operação aberta")
    with col3:
        st.write(f"Saldo Atual: {account['balance']}")

# =========================
# RELATÓRIOS PROFISSIONAIS
# =========================
elif menu=="Reports":
    st.header("Relatórios Profissionais Flutuantes")
    periodo = st.selectbox("Período", ["Diário","Semanal","Mensal","Anual"])
    relatorio = {
        "Período":periodo,
        "Data":datetime.today().strftime("%Y-%m-%d"),
        "ResumoMétricas":market_metrics,
        "Alertas":[a['message'] for a in advisor.alerts[-10:]],
        "Sugestões":["Monitorar WaveScaling","Revisar Momentum"]
    }
    st.write(relatorio)

# =========================
# APPS DOWNLOAD
# =========================
elif menu=="Apps":
    st.header("Download STP-X1 Global Pro")
    st.download_button("App Desktop", data="STPX1 Desktop", file_name="STPX1_desktop.zip")
    st.download_button("App Mobile", data="STPX1 Mobile", file_name="STPX1_mobile.apk")

# =========================
# CONTA / OWNER
# =========================
elif menu=="Account Settings":
    st.header("Conta Proprietário / Planos")
    st.info("Alterar planos, simular experiência de usuário e acessar métricas do Advisor.")
