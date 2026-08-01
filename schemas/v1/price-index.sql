-- ============================================================
-- PayPack Price Index — 价格指数与信用评分系统
-- Version: 1.0.0
-- License: Apache 2.0
-- 
-- 说明：本 Schema 定义了 PayPack 价格指数与商户信用评分的数据结构。
-- 计算公式公开（Tukey's fences + PVI），具体评分权重与反作弊规则
-- 由 PayPack Cloud 管控。
-- ============================================================

-- 1. 服务类型字典
CREATE TABLE IF NOT EXISTS service_type_dict (
    id INT PRIMARY KEY AUTO_INCREMENT,
    service_code VARCHAR(32) UNIQUE NOT NULL COMMENT '服务代码，如 bid_data_query',
    service_name VARCHAR(100) NOT NULL COMMENT '服务名称',
    category VARCHAR(50) DEFAULT 'general' COMMENT '分类',
    is_active TINYINT DEFAULT 1
);

-- 2. 每日价格指数快照
CREATE TABLE IF NOT EXISTS price_index_daily (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    service_code VARCHAR(32) NOT NULL COMMENT '服务代码',
    stat_date DATE NOT NULL COMMENT '统计日期',
    benchmark_price DECIMAL(18,6) NOT NULL COMMENT '基准价（中位数）',
    p25_price DECIMAL(18,6) NOT NULL COMMENT '25分位数',
    p75_price DECIMAL(18,6) NOT NULL COMMENT '75分位数',
    fair_lower DECIMAL(18,6) NOT NULL COMMENT '公允区间下限 = P25 - 1.5*IQR',
    fair_upper DECIMAL(18,6) NOT NULL COMMENT '公允区间上限 = P75 + 1.5*IQR',
    pvi DECIMAL(10,4) DEFAULT 0.0000 COMMENT '价格波动指数(%)',
    sample_count INT DEFAULT 0 COMMENT '有效样本数',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_service_date (service_code, stat_date),
    KEY idx_date (stat_date)
);

-- 3. 商户信用评分
CREATE TABLE IF NOT EXISTS merchant_risk_score (
    merchant_id VARCHAR(64) PRIMARY KEY COMMENT '商户ID',
    trust_score INT DEFAULT 50 COMMENT '综合信用分 0-100',
    avg_price_7d DECIMAL(18,6) DEFAULT 0 COMMENT '近7天均价',
    price_integrity_score INT DEFAULT 50 COMMENT '价格诚信分 0-100',
    price_deviation_rate DECIMAL(10,4) DEFAULT 0 COMMENT '价格偏离基准的比率',
    dispute_rate DECIMAL(8,6) DEFAULT 0 COMMENT '争议率（近30天）',
    uptime_pct DECIMAL(5,2) DEFAULT 0 COMMENT '近30天服务可用率(%)',
    total_calls_24h INT DEFAULT 0 COMMENT '近24h调用量',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 4. 用户反馈（众包评分）
CREATE TABLE IF NOT EXISTS user_feedback (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    order_id VARCHAR(64) NOT NULL COMMENT '关联交易ID',
    user_id VARCHAR(64) COMMENT '评价者',
    merchant_id VARCHAR(64) NOT NULL COMMENT '被评商户',
    rating TINYINT NOT NULL CHECK (rating BETWEEN 1 AND 5) COMMENT '1-5星',
    price_fair TINYINT COMMENT '价格是否合理 1-5',
    comment TEXT COMMENT '文字评价',
    screenshot_url VARCHAR(512) COMMENT '截图URL（供AI核验）',
    is_verified TINYINT DEFAULT 0 COMMENT '是否通过AI核验',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    KEY idx_merchant (merchant_id),
    KEY idx_order (order_id)
);

-- 核心计算公式（公开）
-- 
-- 公允价格区间 (Tukey's fences):
--   IQR = P75 - P25
--   fair_lower = max(0, P25 - 1.5 * IQR)
--   fair_upper = P75 + 1.5 * IQR
--
-- 价格波动指数:
--   PVI = (当日基准价 - N日前基准价) / N日前基准价 × 100%
--
-- 商户价格诚信分（权重与 credit-score.json 一致，以 Schema 为准）:
--   score = 40% × (1 - avg|价格偏离度|) + 30% × 用户价格合理性评分均值 + 30% × 履约率评分
