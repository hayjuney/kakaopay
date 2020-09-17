/* 더치페이를 요청한 유저 중
A 가맹점에서 2019년 12월에 1만원 이상 결제한 유저 user_id
2019년 12월 결제분 중 취소를 반영한 순결제금액 1만원 이상인 유저만을 대상으로 함
취소 반영기간은 2020년 2월까지로 함 */

WITH paid AS (
	SELECT user_id, transaction_id, amount
	  FROM a_payment_trx
	  JOIN dutchpay_claim ON dutchpay_claim.claim_user_id = a_payment_trx.user_id
	 WHERE payment_action_type = 'PAYMENT' AND YEAR(transacted_at) = 2019 AND MONTH(transacted_at) = 12
), cancelled AS (
	SELECT transaction_id, amount
	WHERE payment_action_type = 'CANCELLED' AND transacted_at < '2020-03-01'
), temp AS (
	SELECT paid.user_id AS user_id,
		   SUM(paid.amount) AS paid_sum,
		   SUM(cancelled.amount) AS cancelled_sum
	  FROM paid
 LEFT JOIN cancelled ON cancelled.transaction_id = paid.transaction_id
  GROUP BY 1
)
	SELECT user_id FROM temp
	WHERE paid_sum - cancelled_sum >= 10000