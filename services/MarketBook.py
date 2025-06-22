from typing import Mapping, Optional, List
import logging
import os
import datetime

from utils.utils import unix_to_utc, load_raw_data
import copy

class MarketBook():
    def __init__(
        self,
        asset_id: str,
        book_name: str,
        fp_data: str,
    ) -> None:
        self._fp_data = fp_data
        self._asset_id = asset_id
        self._book_name = book_name

        self._states = self._generate_states(
            self._fp_data,
            self._asset_id,
        )

    def _generate_states(
        self,
        fp_data: str,
        asset_id: str,
    ) -> List[Mapping]:
        updates = self._get_updates(fp_data, asset_id)

        states = [None]

        for update in updates:
            valid_types = {
                "price_change",
                "book",
            }

            if update["event_type"] not in valid_types:
                continue

            timestamp = update["timestamp"]

            latest_state = self._update(
                update,
                states[-1],
            )

            latest_state["timestamp"] = timestamp

            states.append(latest_state)

        return states

    def _get_updates(
        self,
        fp_data: str,
        asset_id: str,
    ) -> List[Mapping]:
        data = [
            _ for _ in load_raw_data(fp_data) if
            _["asset_id"] == asset_id
        ]
        return data
    
    def _update(
        self,
        update: Mapping,
        previous_state: Optional[Mapping] = None,
    ) -> Mapping:
        if update["event_type"] == "book":
            return self._construct_book(update)
        
        if not previous_state:
            raise ValueError("Non-book update events require a previous state")
        
        next_state = copy.deepcopy(previous_state)

        for change in update["changes"]:
            price, side, size = change["price"], change["side"], change["size"]

            target = "bids" if side == "BUY" else "asks"
            counter_target = "asks" if side == "BUY" else "bids"

            updated = False

            for i, price_dict in enumerate(next_state[target]):
                if price_dict["price"] == price and size == "0":
                    next_state[target].pop(i)
                    updated = True
                    break
                elif price_dict["price"] == price:
                    price_dict["size"] = str(size)
                    updated = True
                    break

            for i, price_dict in enumerate(next_state[counter_target]):
                if price_dict["price"] == price:
                    size_diff = round(
                        float(price_dict["size"]) - float(size),
                        3
                    )

                    if size_diff == 0:
                        next_state[counter_target].pop(i)
                    elif size_diff > 0:
                        price_dict["size"] = size_diff
                    else:
                        next_state[target].append(
                            {
                                "price": price,
                                "size": str(-size_diff),
                            }
                        )
                    
                    updated = True
                    break

            if updated:
                continue

            next_state[target].append(
                {
                    "price": price,
                    "size": size,
                }
            )

        next_state["bids"] = sorted(next_state["bids"], key=lambda x: float(x["price"]))
        next_state["asks"] = sorted(next_state["asks"], key=lambda x: float(x["price"]))

        return next_state

    def _construct_book(
        self,
        update: Mapping,
    ) -> Mapping:
        if update["event_type"] != "book":
            raise ValueError(
                "Book construction got unexpected event update type:" +
                f" {update['event_type']}"
            )
        
        update["bids"] =  sorted(update["bids"], key=lambda x: float(x["price"]))
        update["asks"] =  sorted(update["asks"], key=lambda x: float(x["price"]))

        return update
    
    def display_book(
        self,
        index: int,
    ) -> None:
        if index < 0:
            print("Enter non-negative index")
            return
        elif index >= len(self._states):
            print("Index out of range")
            return

        book = self._states[index]

        bids = book["bids"]
        asks = book["asks"]
        timestamp = unix_to_utc(book["timestamp"])

        print(f"UTC: {timestamp}")
        print(f"==={self._book_name}===")

        print("TYPE\tPRICE\tSIZE")

        if len(asks) != 0:
            for ask in asks[::-1]:
                price, size = ask["price"], ask["size"]
                print(f"ASK\t{price}\t{size}")

        if len(asks) != 0 and len(bids) != 0:
            spread = float(asks[0]["price"]) - float(bids[-1]["price"])
            price = (float(asks[0]["price"]) + float(bids[-1]["price"]))/2.0
            print(f"-----SPREAD: {spread:.3f}  PRICE: {price:.3f}-----")
        else:
            print("-----SPREAD: INVALID  PRICE: INVALID-----")

        if len(bids) != 0:
            for bid in bids[::-1]:
                price, size = bid["price"], bid["size"]
                print(f"BID\t{price}\t{size}")

    def __getitem__(
        self,
        index: int,
    ) -> Mapping:
        return self._states[index]
    
    def __len__(
        self,
    ):
        return(len(self._states))

