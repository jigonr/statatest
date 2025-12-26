*! fixture_bipartite_network.ado
*! Version 1.0.0
*! Creates a bipartite network (seller-buyer) for testing
*! Based on Bernard & Zi (2022) elementary model structure
*!
*! Syntax:
*!   fixture_bipartite_network [, n_firms(#) n_edges(#) temporal seed(#)]
*!
*! Options:
*!   n_firms(#)  - Total number of firms (default: 100)
*!   n_edges(#)  - Number of edges/transactions (default: 500)
*!   temporal    - Add year dimension (2015-2019)
*!   seed(#)     - Random seed (default: 12345)
*!
*! Creates variables:
*!   seller  - Seller firm ID
*!   buyer   - Buyer firm ID  
*!   weight  - Transaction value (log-normal)
*!   year    - Time period (if temporal option specified)
*!
*! Structure follows Bernard & Zi (2022):
*!   ~31% only buyers, ~13% only sellers, ~56% both

program define fixture_bipartite_network
    version 16
    
    syntax [, n_firms(integer 100) n_edges(integer 500) temporal seed(integer 12345)]
    
    clear
    set seed `seed'
    
    // Firm composition (Bernard & Zi 2022)
    local n_only_buyers = floor(0.31 * `n_firms')
    local n_only_sellers = floor(0.13 * `n_firms')
    local n_both = `n_firms' - `n_only_buyers' - `n_only_sellers'
    
    // Seller pool: only_sellers + both
    local n_sellers = `n_only_sellers' + `n_both'
    // Buyer pool: only_buyers + both  
    local n_buyers = `n_only_buyers' + `n_both'
    
    // Create edges
    if "`temporal'" != "" {
        local n_years = 5
        local total_edges = `n_edges' * `n_years'
    }
    else {
        local total_edges = `n_edges'
    }
    
    set obs `total_edges'
    
    // Generate seller IDs (from seller pool)
    gen int seller = ceil(runiform() * `n_sellers')
    
    // Generate buyer IDs (from buyer pool, offset by n_only_sellers)
    gen int buyer = `n_only_sellers' + ceil(runiform() * `n_buyers')
    
    // Ensure no self-loops (seller != buyer)
    replace buyer = buyer + 1 if seller == buyer
    replace buyer = `n_only_sellers' + 1 if buyer > `n_firms'
    
    // Transaction weight (log-normal, mean ~0.034, following BCCR data)
    gen double weight = exp(rnormal(-3.4, 0.5))
    
    // Add temporal dimension if requested
    if "`temporal'" != "" {
        gen int year = 2015 + floor((_n - 1) / `n_edges')
        label variable year "Transaction year"
    }
    
    // Remove exact duplicates (keep unique edges per period)
    if "`temporal'" != "" {
        duplicates drop seller buyer year, force
    }
    else {
        duplicates drop seller buyer, force
    }
    
    // Labels
    label variable seller "Seller firm ID"
    label variable buyer "Buyer firm ID"
    label variable weight "Transaction value"
    
    // Return info
    quietly count
    return scalar n_edges = r(N)
    return scalar n_firms = `n_firms'
    return scalar n_sellers = `n_sellers'
    return scalar n_buyers = `n_buyers'
end

// Alias for production network naming
program define fixture_production_network
    fixture_bipartite_network `0'
end

// Alias for trade network
program define fixture_trade_network
    fixture_bipartite_network `0'
end
