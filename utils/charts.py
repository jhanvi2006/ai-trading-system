import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def create_candlestick(df, stock, range_option):

    if range_option == "1W":
        df_plot = df.tail(7)
    elif range_option == "1M":
        df_plot = df.tail(30)
    elif range_option == "3M":
        df_plot = df.tail(90)
    else:
        df_plot = df

    fig = go.Figure()

    # Candlestick
    fig.add_trace(go.Candlestick(
        x=df_plot['Date'],
        open=df_plot['Open'],
        high=df_plot['High'],
        low=df_plot['Low'],
        close=df_plot['Close'],
        increasing_line_color='#00ff88',
        decreasing_line_color='#ff4444',
        name="Price"
    ))

    # Volume Bars
    fig.add_trace(go.Bar(
        x=df_plot['Date'], 
        y=df_plot.get('Volume', np.random.randint(1000000,5000000,len(df_plot))),  # Fallback if no Volume
        name="Volume",
        yaxis='y2',
        marker_color='rgba(128,0,128,0.6)',
        opacity=0.7
    ))

    # MA10 and MA20
    fig.add_trace(go.Scatter(
        x=df_plot['Date'],
        y=df_plot['MA_10'],
        mode='lines',
        name='MA10',
        line=dict(color='orange', width=2)
    ))

    # Use pre-computed RSI
    fig.add_trace(go.Scatter(
        x=df_plot['Date'],
        y=df_plot['RSI'],
        mode='lines',
        name='RSI',
        line=dict(color='purple', width=1, dash='dot'),
        yaxis='y3'
    ))

    fig.update_layout(
        title=f"📊 {stock} - Advanced Chart ({range_option})",
        template="plotly_dark",
        height=600,
        xaxis_rangeslider_visible=True,
        yaxis=dict(title="Price", side="left"),
        yaxis2=dict(title="Volume", overlaying="y", side="right", showgrid=False),
        yaxis3=dict(title="RSI", overlaying="y", side="right", position=0.95, anchor="free", range=[0,100]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='x unified'
    )

    return fig
