def initialize_portfolio(st):

    if "balance" not in st.session_state:
        st.session_state.balance = 10000.0
        st.session_state.initial_balance = 10000.0
        st.session_state.portfolio = {}

def buy_stock(st, stock, price):

    if st.session_state.balance >= price:
        st.session_state.balance -= price
        st.session_state.portfolio[stock] = st.session_state.portfolio.get(stock, 0) + 1

def sell_stock(st, stock, price):

    if st.session_state.portfolio.get(stock, 0) > 0:
        st.session_state.balance += price
        st.session_state.portfolio[stock] -= 1

def calculate_portfolio_value(portfolio, current_prices):

    return sum(v * current_prices.get(k, 0) for k, v in portfolio.items())