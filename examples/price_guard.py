"""
PayPack Price Guard — 价格风控守卫（开源示例）

在 PayPack 支付流程中插入价格检查钩子。
超时或服务异常时自动降级放行，不影响主流程。

License: Apache 2.0
Usage:
    from price_guard import check_price_sync

    result = check_price_sync("bid_data_query", amount=0.50, merchant_id="m001")
    if not result.allowed:
        return {"error": "PRICE_BLOCKED", "message": result.message}
"""

import logging
from datetime import datetime
from typing import Optional, Dict, Tuple

logger = logging.getLogger(__name__)


class PriceCheckResult:
    """价格检查结果"""

    def __init__(
        self,
        allowed: bool,
        level: str,
        message: str,
        benchmark: Optional[float] = None,
        fair_range: Optional[Tuple[float, float]] = None,
        raw_data: Optional[Dict] = None,
    ):
        self.allowed = allowed  # True=放行, False=拦截
        self.level = level      # normal | warning | abnormal | error | disabled
        self.message = message
        self.benchmark = benchmark
        self.fair_range = fair_range
        self.raw_data = raw_data
        self.checked_at = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict:
        return {
            "allowed": self.allowed,
            "level": self.level,
            "message": self.message,
            "benchmark": self.benchmark,
            "fair_range": self.fair_range,
            "checked_at": self.checked_at,
        }


# ========== 配置（按需覆盖） ==========
PRICE_INDEX_ENABLED = True
PRICE_INDEX_API_URL = "http://localhost:8010/v1/price_advice"
PRICE_CHECK_TIMEOUT = 1.5          # 秒，超时则降级放行
PRICE_ABNORMAL_THRESHOLD = 2.0    # 公允上限的倍数，超过则拦截


# ========== 核心检查函数 ==========

def check_price_sync(
    service_code: str,
    amount: float,
    merchant_id: Optional[str] = None,
) -> PriceCheckResult:
    """
    支付前检查价格是否合理。

    调用价格指数引擎 API，将当前金额与公允区间对比。
    如果引擎不可用，自动降级放行（fail-open）。
    """
    if not PRICE_INDEX_ENABLED or amount <= 0:
        return PriceCheckResult(True, "disabled", "价格风控未启用或金额无效")

    try:
        import httpx

        with httpx.Client(timeout=PRICE_CHECK_TIMEOUT) as client:
            resp = client.get(
                PRICE_INDEX_API_URL,
                params={"service_code": service_code, "merchant_id": merchant_id},
            )

        if resp.status_code != 200:
            logger.warning(f"价格指数API异常 HTTP {resp.status_code}，降级放行")
            return PriceCheckResult(True, "error", "价格指数服务异常，已降级放行")

        data = resp.json()
        if not data:
            return PriceCheckResult(True, "error", "暂无价格指数数据，已放行")

        benchmark = data.get("benchmark", 0)
        fair_range = data.get("fair_range", [0, 0])
        lower, upper = fair_range[0], fair_range[1] if len(fair_range) > 1 else float("inf")

        # 价格区间判断
        if lower <= amount <= upper:
            return PriceCheckResult(
                True, "normal",
                f"价格在公允区间 [{lower:.4f}, {upper:.4f}] 内",
                benchmark, (lower, upper), data,
            )

        if amount <= upper * PRICE_ABNORMAL_THRESHOLD:
            logger.info(f"[PRICE_WARNING] {service_code}: {amount} > 基准 {benchmark}")
            return PriceCheckResult(
                True, "warning",
                f"价格略高于市场基准 {benchmark:.2f}，建议比价",
                benchmark, (lower, upper), data,
            )

        logger.warning(f"[PRICE_BLOCKED] {service_code}: {amount} >> 基准 {benchmark}")
        return PriceCheckResult(
            False, "abnormal",
            f"价格异常偏高，已拦截（基准: {benchmark:.2f}，公允上限: {upper:.2f}）",
            benchmark, (lower, upper), data,
        )

    except Exception as e:
        logger.warning(f"价格检查异常: {e}，降级放行")
        return PriceCheckResult(True, "error", f"价格检查异常: {str(e)[:80]}，已降级放行")


# ========== 集成示例 ==========
# 在 PayPack 的 pay() 方法中插入：
#
#   from price_guard import check_price_sync
#
#   result = check_price_sync(service_code, amount, merchant_id)
#   if not result.allowed:
#       return {"success": False, "code": "PRICE_BLOCKED", "message": result.message}
#   # ... 继续支付 ...

if __name__ == "__main__":
    # 独立测试
    r = check_price_sync("bid_data_query", 0.50, "m001")
    print(f"结果: allowed={r.allowed}, level={r.level}, message={r.message}")
