USE ecommerce_analytics;
SELECT
    COUNT(DISTINCT session_id) AS total_sessions,
    COUNT(DISTINCT CASE WHEN event_name = 'page_view' THEN session_id END) AS page_views,
    COUNT(DISTINCT CASE WHEN event_name = 'pdp_view' THEN session_id END) AS pdp_views,
    COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' THEN session_id END) AS add_to_cart,
    COUNT(DISTINCT CASE WHEN event_name = 'checkout_start' THEN session_id END) AS checkout_start,
    COUNT(DISTINCT CASE WHEN event_name = 'payment_initiated' THEN session_id END) AS payment_initiated,
    COUNT(DISTINCT CASE WHEN event_name = 'order_placed' THEN session_id END) AS orders
FROM events;

SELECT
    ROUND(100.0 * 413403 / 500000, 2) AS session_to_pdp_cvr,
    ROUND(100.0 * 141151 / 413403, 2) AS pdp_to_cart_cvr,
    ROUND(100.0 * 72945 / 141151, 2) AS cart_to_checkout_cvr,
    ROUND(100.0 * 54248 / 72945, 2) AS checkout_to_payment_cvr,
    ROUND(100.0 * 43637 / 54248, 2) AS payment_to_order_cvr,
    ROUND(100.0 * 43637 / 500000, 2) AS overall_cvr;
    
    SELECT
    s.device,
    COUNT(DISTINCT s.session_id) AS total_sessions,
    COUNT(DISTINCT CASE WHEN e.event_name = 'pdp_view' THEN s.session_id END) AS pdp_views,
    COUNT(DISTINCT CASE WHEN e.event_name = 'add_to_cart' THEN s.session_id END) AS add_to_cart,
    COUNT(DISTINCT CASE WHEN e.event_name = 'checkout_start' THEN s.session_id END) AS checkout_start,
    COUNT(DISTINCT CASE WHEN e.event_name = 'payment_initiated' THEN s.session_id END) AS payment_initiated,
    COUNT(DISTINCT CASE WHEN e.event_name = 'order_placed' THEN s.session_id END) AS orders
FROM sessions s
LEFT JOIN events e
    ON s.session_id = e.session_id
GROUP BY s.device
ORDER BY total_sessions DESC;

SELECT
    s.device,
    ROUND(
        100.0 * COUNT(DISTINCT CASE WHEN e.event_name = 'pdp_view' THEN s.session_id END)
        / COUNT(DISTINCT s.session_id), 2
    ) AS session_to_pdp_cvr,

    ROUND(
        100.0 * COUNT(DISTINCT CASE WHEN e.event_name = 'add_to_cart' THEN s.session_id END)
        / COUNT(DISTINCT CASE WHEN e.event_name = 'pdp_view' THEN s.session_id END), 2
    ) AS pdp_to_cart_cvr,

    ROUND(
        100.0 * COUNT(DISTINCT CASE WHEN e.event_name = 'checkout_start' THEN s.session_id END)
        / COUNT(DISTINCT CASE WHEN e.event_name = 'add_to_cart' THEN s.session_id END), 2
    ) AS cart_to_checkout_cvr,

    ROUND(
        100.0 * COUNT(DISTINCT CASE WHEN e.event_name = 'payment_initiated' THEN s.session_id END)
        / COUNT(DISTINCT CASE WHEN e.event_name = 'checkout_start' THEN s.session_id END), 2
    ) AS checkout_to_payment_cvr,

    ROUND(
        100.0 * COUNT(DISTINCT CASE WHEN e.event_name = 'order_placed' THEN s.session_id END)
        / COUNT(DISTINCT CASE WHEN e.event_name = 'payment_initiated' THEN s.session_id END), 2
    ) AS payment_to_order_cvr

FROM sessions s
LEFT JOIN events e
    ON s.session_id = e.session_id
GROUP BY s.device
ORDER BY s.device;

SELECT
    ROUND(MAX(CASE WHEN s.device = 'Desktop' THEN cart_to_checkout_cvr END), 2) AS desktop_cvr,
    ROUND(MAX(CASE WHEN s.device = 'Mobile' THEN cart_to_checkout_cvr END), 2) AS mobile_cvr,
    ROUND(
        MAX(CASE WHEN s.device = 'Desktop' THEN cart_to_checkout_cvr END)
        -
        MAX(CASE WHEN s.device = 'Mobile' THEN cart_to_checkout_cvr END),
        2
    ) AS desktop_mobile_gap_pp
FROM (
    SELECT
        s.device,
        100.0 * COUNT(DISTINCT CASE WHEN e.event_name = 'checkout_start' THEN s.session_id END)
        / COUNT(DISTINCT CASE WHEN e.event_name = 'add_to_cart' THEN s.session_id END)
        AS cart_to_checkout_cvr
    FROM sessions s
    LEFT JOIN events e
        ON s.session_id = e.session_id
    GROUP BY s.device
) x;

SELECT
    ROUND(MAX(CASE WHEN x.device = 'Desktop' THEN x.cart_to_checkout_cvr END), 2) AS desktop_cvr,
    ROUND(MAX(CASE WHEN x.device = 'Mobile' THEN x.cart_to_checkout_cvr END), 2) AS mobile_cvr,
    ROUND(
        MAX(CASE WHEN x.device = 'Desktop' THEN x.cart_to_checkout_cvr END)
        -
        MAX(CASE WHEN x.device = 'Mobile' THEN x.cart_to_checkout_cvr END),
        2
    ) AS desktop_mobile_gap_pp
FROM (
    SELECT
        s.device,
        100.0 * COUNT(DISTINCT CASE WHEN e.event_name = 'checkout_start' THEN s.session_id END)
        / COUNT(DISTINCT CASE WHEN e.event_name = 'add_to_cart' THEN s.session_id END)
        AS cart_to_checkout_cvr
    FROM sessions s
    LEFT JOIN events e
        ON s.session_id = e.session_id
    GROUP BY s.device
) x;

SELECT
    ROUND(MAX(CASE WHEN x.device = 'Desktop' THEN x.cart_to_checkout_cvr END), 2) AS desktop_cvr,
    ROUND(MAX(CASE WHEN x.device = 'Mobile' THEN x.cart_to_checkout_cvr END), 2) AS mobile_cvr,
    ROUND(
        MAX(CASE WHEN x.device = 'Desktop' THEN x.cart_to_checkout_cvr END)
        -
        MAX(CASE WHEN x.device = 'Mobile' THEN x.cart_to_checkout_cvr END),
        2
    ) AS desktop_mobile_gap_pp
FROM (
    SELECT
        s.device,
        100.0 * COUNT(DISTINCT CASE WHEN e.event_name = 'checkout_start' THEN s.session_id END)
        / COUNT(DISTINCT CASE WHEN e.event_name = 'add_to_cart' THEN s.session_id END)
        AS cart_to_checkout_cvr
    FROM sessions s
    LEFT JOIN events e
        ON s.session_id = e.session_id
    GROUP BY s.device
) x;

SELECT
    COUNT(DISTINCT CASE
        WHEN e.event_name = 'add_to_cart'
        THEN e.session_id
    END) AS add_to_cart_sessions,

    COUNT(DISTINCT CASE
        WHEN e.event_name = 'checkout_start'
        THEN e.session_id
    END) AS checkout_sessions,

    COUNT(DISTINCT CASE
        WHEN e.event_name = 'add_to_cart'
        THEN e.session_id
    END)
    -
    COUNT(DISTINCT CASE
        WHEN e.event_name = 'checkout_start'
        THEN e.session_id
    END) AS abandoned_cart_sessions,

    ROUND(
        100.0 *
        (
            COUNT(DISTINCT CASE
                WHEN e.event_name = 'add_to_cart'
                THEN e.session_id
            END)
            -
            COUNT(DISTINCT CASE
                WHEN e.event_name = 'checkout_start'
                THEN e.session_id
            END)
        )
        /
        COUNT(DISTINCT CASE
            WHEN e.event_name = 'add_to_cart'
            THEN e.session_id
        END),
        2
    ) AS cart_abandonment_rate

FROM events e;

SELECT
    COUNT(*) AS total_orders,
    ROUND(SUM(order_value), 2) AS total_gmv,
    ROUND(AVG(order_value), 2) AS average_order_value
FROM orders;


SELECT
    68206 AS abandoned_cart_sessions,
    2640.27 AS average_order_value,
    10 AS recovery_rate_percent,
    ROUND(68206 * 2640.27 * 0.10, 2) AS potential_gmv_recovery;
    
    SELECT
    recovery_rate,
    ROUND(68206 * 2640.27 * recovery_rate / 100, 2) AS potential_gmv_recovery
FROM (
    SELECT 0 AS recovery_rate
    UNION ALL SELECT 5
    UNION ALL SELECT 10
    UNION ALL SELECT 15
    UNION ALL SELECT 20
) AS recovery_scenarios
ORDER BY recovery_rate;

SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    COUNT(*) AS total_orders,
    ROUND(SUM(order_value), 2) AS total_gmv,
    ROUND(AVG(order_value), 2) AS average_order_value
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;

SELECT
    s.channel,
    COUNT(DISTINCT s.session_id) AS total_sessions,
    COUNT(DISTINCT CASE
        WHEN e.event_name = 'order_placed'
        THEN s.session_id
    END) AS orders,
    ROUND(
        100.0 * COUNT(DISTINCT CASE
            WHEN e.event_name = 'order_placed'
            THEN s.session_id
        END)
        / COUNT(DISTINCT s.session_id),
        2
    ) AS conversion_rate
FROM sessions s
LEFT JOIN events e
    ON s.session_id = e.session_id
GROUP BY s.channel
ORDER BY conversion_rate DESC;

SELECT
    s.category,
    COUNT(DISTINCT s.session_id) AS total_sessions,
    COUNT(DISTINCT CASE
        WHEN e.event_name = 'pdp_view'
        THEN s.session_id
    END) AS pdp_views,
    COUNT(DISTINCT CASE
        WHEN e.event_name = 'add_to_cart'
        THEN s.session_id
    END) AS add_to_cart,
    COUNT(DISTINCT CASE
        WHEN e.event_name = 'checkout_start'
        THEN s.session_id
    END) AS checkout_start,
    COUNT(DISTINCT CASE
        WHEN e.event_name = 'order_placed'
        THEN s.session_id
    END) AS orders,
    ROUND(
        100.0 * COUNT(DISTINCT CASE
            WHEN e.event_name = 'order_placed'
            THEN s.session_id
        END)
        / COUNT(DISTINCT s.session_id),
        2
    ) AS conversion_rate
FROM sessions s
LEFT JOIN events e
    ON s.session_id = e.session_id
GROUP BY s.category
ORDER BY conversion_rate DESC;


SELECT
    category,
    COUNT(*) AS total_orders,
    ROUND(SUM(order_value), 2) AS total_gmv,
    ROUND(AVG(order_value), 2) AS average_order_value
FROM orders
GROUP BY category
ORDER BY total_gmv DESC;

SELECT
    s.device,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(o.order_value), 2) AS total_gmv,
    ROUND(AVG(o.order_value), 2) AS average_order_value
FROM orders o
JOIN sessions s
    ON o.session_id = s.session_id
GROUP BY s.device
ORDER BY total_gmv DESC;


SELECT
    s.hour,
    COUNT(DISTINCT s.session_id) AS total_sessions,
    COUNT(DISTINCT CASE
        WHEN e.event_name = 'order_placed'
        THEN s.session_id
    END) AS orders,
    ROUND(
        100.0 * COUNT(DISTINCT CASE
            WHEN e.event_name = 'order_placed'
            THEN s.session_id
        END)
        / COUNT(DISTINCT s.session_id),
        2
    ) AS conversion_rate
FROM sessions s
LEFT JOIN events e
    ON s.session_id = e.session_id
GROUP BY s.hour
ORDER BY s.hour;


WITH session_metrics AS (
    SELECT
        session_id,
        TIMESTAMPDIFF(
            SECOND,
            MIN(event_time),
            MAX(event_time)
        ) AS session_duration_seconds,

        MAX(
            CASE
                WHEN event_name = 'order_placed'
                THEN 1
                ELSE 0
            END
        ) AS converted
    FROM events
    GROUP BY session_id
)

SELECT
    converted,
    COUNT(*) AS total_sessions,
    ROUND(AVG(session_duration_seconds), 2) AS avg_session_duration_seconds
FROM session_metrics
GROUP BY converted
ORDER BY converted;


SELECT
    category,
    COUNT(*) AS total_orders,
    ROUND(SUM(order_value), 2) AS total_gmv,
    RANK() OVER (ORDER BY SUM(order_value) DESC) AS gmv_rank
FROM orders
GROUP BY category
ORDER BY gmv_rank;

SELECT
    s.device,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(o.order_value), 2) AS total_gmv,
    ROUND(AVG(o.order_value), 2) AS average_order_value
FROM orders o
JOIN sessions s
    ON o.session_id = s.session_id
GROUP BY s.device
ORDER BY total_gmv DESC;


SELECT
    s.channel,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(o.order_value), 2) AS total_gmv,
    ROUND(AVG(o.order_value), 2) AS average_order_value
FROM orders o
JOIN sessions s
    ON o.session_id = s.session_id
GROUP BY s.channel
ORDER BY total_gmv DESC;

SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    COUNT(*) AS total_orders,
    ROUND(SUM(order_value), 2) AS total_gmv,
    ROUND(AVG(order_value), 2) AS average_order_value
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;


SELECT
    s.category,
    s.device,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(o.order_value), 2) AS total_gmv
FROM orders o
JOIN sessions s
    ON o.session_id = s.session_id
GROUP BY
    s.category,
    s.device
ORDER BY
    s.category,
    total_gmv DESC;
    
    
    SELECT
    s.category,
    s.device,
    
    COUNT(DISTINCT s.session_id) AS total_sessions,

    COUNT(DISTINCT CASE
        WHEN e.event_name = 'add_to_cart'
        THEN s.session_id
    END) AS add_to_cart_sessions,

    COUNT(DISTINCT CASE
        WHEN e.event_name = 'checkout_start'
        THEN s.session_id
    END) AS checkout_sessions,

    ROUND(
        100.0 *
        COUNT(DISTINCT CASE
            WHEN e.event_name = 'checkout_start'
            THEN s.session_id
        END)
        /
        NULLIF(
            COUNT(DISTINCT CASE
                WHEN e.event_name = 'add_to_cart'
                THEN s.session_id
            END), 0
        ),
        2
    ) AS cart_to_checkout_cvr

FROM sessions s
LEFT JOIN events e
    ON s.session_id = e.session_id

GROUP BY
    s.category,
    s.device

ORDER BY
    cart_to_checkout_cvr ASC;
    
    
    SELECT
    ROUND(
        100.0 *
        SUM(CASE
            WHEN s.device = 'Desktop'
            AND e.event_name = 'checkout_start'
            THEN 1 ELSE 0
        END)
        /
        NULLIF(
            SUM(CASE
                WHEN s.device = 'Desktop'
                AND e.event_name = 'add_to_cart'
                THEN 1 ELSE 0
            END), 0
        ),
        2
    ) AS desktop_cvr,

    ROUND(
        100.0 *
        SUM(CASE
            WHEN s.device = 'Mobile'
            AND e.event_name = 'checkout_start'
            THEN 1 ELSE 0
        END)
        /
        NULLIF(
            SUM(CASE
                WHEN s.device = 'Mobile'
                AND e.event_name = 'add_to_cart'
                THEN 1 ELSE 0
            END), 0
        ),
        2
    ) AS mobile_cvr;
    
    
    SELECT
    s.device,

    COUNT(DISTINCT s.session_id) AS total_sessions,

    COUNT(DISTINCT CASE
        WHEN e.event_name = 'add_to_cart'
        THEN s.session_id
    END) AS add_to_cart_sessions,

    COUNT(DISTINCT CASE
        WHEN e.event_name = 'checkout_start'
        THEN s.session_id
    END) AS checkout_sessions,

    ROUND(
        100.0 *
        COUNT(DISTINCT CASE
            WHEN e.event_name = 'checkout_start'
            THEN s.session_id
        END)
        /
        NULLIF(
            COUNT(DISTINCT CASE
                WHEN e.event_name = 'add_to_cart'
                THEN s.session_id
            END),
            0
        ),
        2
    ) AS cart_to_checkout_cvr

FROM sessions s
LEFT JOIN events e
    ON s.session_id = e.session_id

GROUP BY s.device
ORDER BY cart_to_checkout_cvr DESC;

SELECT
    0 AS recovery_rate,
    0 AS potential_gmv_recovery

UNION ALL

SELECT
    5 AS recovery_rate,
    ROUND(68206 * 2640.27 * 0.05, 2)

UNION ALL

SELECT
    10 AS recovery_rate,
    ROUND(68206 * 2640.27 * 0.10, 2)

UNION ALL

SELECT
    15 AS recovery_rate,
    ROUND(68206 * 2640.27 * 0.15, 2)

UNION ALL

SELECT
    20 AS recovery_rate,
    ROUND(68206 * 2640.27 * 0.20, 2);
    
    
    SELECT
    s.device,
    COUNT(DISTINCT CASE
        WHEN e.event_name = 'add_to_cart' THEN s.session_id
    END) AS add_to_cart_sessions,

    COUNT(DISTINCT CASE
        WHEN e.event_name = 'checkout_start' THEN s.session_id
    END) AS checkout_sessions,

    COUNT(DISTINCT CASE
        WHEN e.event_name = 'add_to_cart' THEN s.session_id
    END)
    -
    COUNT(DISTINCT CASE
        WHEN e.event_name = 'checkout_start' THEN s.session_id
    END) AS abandoned_cart_sessions,

    ROUND(AVG(o.order_value), 2) AS average_order_value,

    ROUND(
        (
            COUNT(DISTINCT CASE
                WHEN e.event_name = 'add_to_cart' THEN s.session_id
            END)
            -
            COUNT(DISTINCT CASE
                WHEN e.event_name = 'checkout_start' THEN s.session_id
            END)
        )
        * AVG(o.order_value) * 0.10,
        2
    ) AS potential_gmv_recovery_10pct

FROM sessions s
LEFT JOIN events e
    ON s.session_id = e.session_id
LEFT JOIN orders o
    ON s.session_id = o.session_id

GROUP BY s.device
ORDER BY potential_gmv_recovery_10pct DESC;



WITH device_orders AS (
    SELECT
        s.device,
        o.order_id,
        o.order_value
    FROM orders o
    JOIN sessions s
        ON o.session_id = s.session_id
)

SELECT
    device,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(order_value), 2) AS total_gmv,
    ROUND(AVG(order_value), 2) AS average_order_value
FROM device_orders
GROUP BY device
ORDER BY total_gmv DESC;

SELECT
    s.device,
    COUNT(o.order_id) AS total_orders,
    ROUND(SUM(o.order_value), 2) AS total_gmv,
    ROUND(
        100.0 * SUM(o.order_value)
        / (SELECT SUM(order_value) FROM orders),
        2
    ) AS gmv_share_pct
FROM orders o
JOIN sessions s
    ON o.session_id = s.session_id
GROUP BY s.device
ORDER BY total_gmv DESC;




WITH funnel AS (
    SELECT
        COUNT(DISTINCT s.session_id) AS total_sessions,

        COUNT(DISTINCT CASE
            WHEN e.event_name = 'pdp_view'
            THEN s.session_id
        END) AS pdp_sessions,

        COUNT(DISTINCT CASE
            WHEN e.event_name = 'add_to_cart'
            THEN s.session_id
        END) AS add_to_cart_sessions,

        COUNT(DISTINCT CASE
            WHEN e.event_name = 'checkout_start'
            THEN s.session_id
        END) AS checkout_sessions,

        COUNT(DISTINCT CASE
            WHEN e.event_name = 'payment_initiated'
            THEN s.session_id
        END) AS payment_sessions,

        COUNT(DISTINCT CASE
            WHEN e.event_name = 'order_placed'
            THEN s.session_id
        END) AS order_sessions

    FROM sessions s
    LEFT JOIN events e
        ON s.session_id = e.session_id
),

revenue AS (
    SELECT
        COUNT(*) AS total_orders,
        ROUND(SUM(order_value), 2) AS total_gmv,
        ROUND(AVG(order_value), 2) AS average_order_value
    FROM orders
),

device_funnel AS (
    SELECT
        s.device,

        COUNT(DISTINCT CASE
            WHEN e.event_name = 'add_to_cart'
            THEN s.session_id
        END) AS add_to_cart_sessions,

        COUNT(DISTINCT CASE
            WHEN e.event_name = 'checkout_start'
            THEN s.session_id
        END) AS checkout_sessions

    FROM sessions s
    LEFT JOIN events e
        ON s.session_id = e.session_id

    GROUP BY s.device
),

device_metrics AS (
    SELECT
        MAX(
            CASE
                WHEN device = 'Desktop'
                THEN 100.0 * checkout_sessions / NULLIF(add_to_cart_sessions, 0)
            END
        ) AS desktop_cart_to_checkout_cvr,

        MAX(
            CASE
                WHEN device = 'Mobile'
                THEN 100.0 * checkout_sessions / NULLIF(add_to_cart_sessions, 0)
            END
        ) AS mobile_cart_to_checkout_cvr

    FROM device_funnel
)

SELECT
    f.total_sessions,

    f.pdp_sessions,

    f.add_to_cart_sessions,

    f.checkout_sessions,

    f.payment_sessions,

    f.order_sessions,

    ROUND(
        100.0 * f.order_sessions / f.total_sessions,
        2
    ) AS overall_conversion_rate,

    ROUND(
        100.0 * f.pdp_sessions / f.total_sessions,
        2
    ) AS session_to_pdp_cvr,

    ROUND(
        100.0 * f.add_to_cart_sessions / f.pdp_sessions,
        2
    ) AS pdp_to_cart_cvr,

    ROUND(
        100.0 * f.checkout_sessions / f.add_to_cart_sessions,
        2
    ) AS cart_to_checkout_cvr,

    ROUND(
        100.0 * f.payment_sessions / f.checkout_sessions,
        2
    ) AS checkout_to_payment_cvr,

    ROUND(
        100.0 * f.order_sessions / f.payment_sessions,
        2
    ) AS payment_to_order_cvr,

    r.total_orders,

    r.total_gmv,

    r.average_order_value,

    f.add_to_cart_sessions - f.checkout_sessions
        AS abandoned_cart_sessions,

    ROUND(
        100.0 *
        (f.add_to_cart_sessions - f.checkout_sessions)
        / f.add_to_cart_sessions,
        2
    ) AS cart_abandonment_rate,

    ROUND(
        (f.add_to_cart_sessions - f.checkout_sessions)
        * r.average_order_value
        * 0.10,
        2
    ) AS potential_gmv_recovery_10pct,

    ROUND(
        dm.desktop_cart_to_checkout_cvr,
        2
    ) AS desktop_cart_to_checkout_cvr,

    ROUND(
        dm.mobile_cart_to_checkout_cvr,
        2
    ) AS mobile_cart_to_checkout_cvr,

    ROUND(
        dm.desktop_cart_to_checkout_cvr
        - dm.mobile_cart_to_checkout_cvr,
        2
    ) AS desktop_mobile_gap_pp

FROM funnel f
CROSS JOIN revenue r
CROSS JOIN device_metrics dm;
