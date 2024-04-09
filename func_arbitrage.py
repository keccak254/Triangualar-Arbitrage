import requests
import json
import time

# Make a Get Request
def get_coin_tickers(url):
    req = requests.get.url
    json_resp = json.loads(req.text)
    return json_resp

# loop through each objects and find the tradeable pairs
def collect_tradeables(json_obj):
    coin_list = []
    for coin in json_obj:
        # isFrozed = json_obj["isFrozed"] # isFrozen changed to state in new Poloniex API
        # is_post_only = json_obj[coin]["postOnly"] # removed in new API from Poloniex
        if coin["state"] == "NORMAL":
            coin_list.append(coin["symbol"])
    return coin_list

# Structure Arbitrage Pairs
def structure_triangular_pairs(coin_list):

    # Declare Variables
    triangular_pairs_list = []
    remove_duplicates_list = []
    pairs_list = coin_list[0:]

    # Get pair A
    for pair_a in pairs_list:
        pair_a_split = pair_a.split("_")
        a_base = pair_a_split[0]
        a_quote = pair_a_split[1]

        # Assing A to Box
        a_pair_box = [a_base, a_quote]

        # Get Pair B
        for pair_b in pairs_list:
            pair_b_split = pair_b.split("_")
            b_base = pair_b_split[0]
            b_quote = pair_b_split[1]

            #Check Pair B
            if pair_b != pair_a:
                if b_base in a_pair_box or b_quote in a_pair_box:

                    # Get Pair C
                    for pair_c in pairs_list:
                        pair_c_split = pair_c.split("_")
                        c_base = pair_c_split[0]
                        c_quote = pair_c_split[1]

                        # Count the number of matching C items
                        if pair_c != pair_a and pair_c != pair_b:
                            combine_all = [pair_a, pair_b, pair_c]
                            pair_box = [a_base, a_quote, b_base, b_quote, c_base, c_quote]

                            counts_c_base = 0
                            for i in pair_box:
                                if i == c_base:
                                    counts_c_base += 1

                            counts_c_quote = 0
                            for i in pair_box:
                                if i == c_quote:
                                    counts_c_quote += 1

                        # Determining Triangular Match
                        if counts_c_base == 2 and counts_c_quote == 2 and c_base != c_quote:
                            combined = pair_a + "." + pair_b + "," + pair_c
                            unique_item = ''.join(sorted(combine_all))

                            if unique_item not in remove_duplicates_list:
                                match_dict = {
                                  "abase": a_base,
                                  "b_base": b_base,
                                  "c_base": c_base,
                                  "a_quote": a_quote,
                                  "b_quote": b_quote,
                                  "c_quote": c_quote,
                                  "pair_a": pair_a,
                                  "pair_b": pair_b,
                                  "pair_c": pair_c,
                                  "combined": combined
                                }
                                triangular_pairs_list.append(match_dict)
                                remove_duplicates_list.append(unique_item)

    # Return result
    return triangular_pairs_list











