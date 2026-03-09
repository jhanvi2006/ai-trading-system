import streamlit as st


def buy_stock(stock, price, quantity):

    cost = price * quantity

    if st.session_state.balance >= cost:

        st.session_state.balance -= cost

        st.session_state.portfolio[stock] = (
            st.session_state.portfolio.get(stock, 0) + quantity
        )

        st.session_state.trade_history.append({
            "Stock": stock,
            "Type": "Buy",
            "Price": price,
            "Quantity": quantity
        })

        st.success("Stock purchased")

    else:
        st.error("Insufficient balance")


def sell_stock(stock, price, quantity):

    owned = st.session_state.portfolio.get(stock, 0)

    if owned >= quantity:

        st.session_state.balance += price * quantity

        st.session_state.portfolio[stock] -= quantity

        st.session_state.trade_history.append({
            "Stock": stock,
            "Type": "Sell",
            "Price": price,
            "Quantity": quantity
        })

        st.success("Stock sold")

    else:
        st.error("Not enough shares")