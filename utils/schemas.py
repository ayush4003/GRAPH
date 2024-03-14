SCHEMAS = {
    'uniswap': '''type Swap @entity(immutable: true) {
  " swap-{ Transaction hash }-{ Log index } "
  id: ID!

  " Transaction hash of the transaction that emitted this event "
  hash: String!

  " Event log index. For transactions that don't emit event, create arbitrary index starting from 0 "
  logIndex: Int!

  " The protocol this transaction belongs to "
  protocol: DexAmmProtocol!

  " Address that received the tokens "
  to: String!

  " Address that sent the tokens "
  from: String!

  " Block number of this event "
  blockNumber: BigInt!

  " Timestamp of this event "
  timestamp: BigInt!

  " Token deposited into pool "
  tokenIn: Token!

  " Amount of token deposited into pool in native units "
  amountIn: BigInt!

  " Amount of token deposited into pool in USD "
  amountInUSD: BigDecimal!

  " Token withdrawn from pool "
  tokenOut: Token!

  " Amount of token withdrawn from pool in native units "
  amountOut: BigInt!

  " Amount of token withdrawn from pool in USD "
  amountOutUSD: BigDecimal!

  " The pool involving this transaction "
  pool: LiquidityPool!
}

type Token @entity {
  " Smart contract address of the token "
  id: Bytes!

  " Name of the token, mirrored from the smart contract "
  name: String!

  " Symbol of the token, mirrored from the smart contract "
  symbol: String!

  " The number of decimal places this token uses, default to 18 "
  decimals: Int!

  " Optional field to track the price of a token, mostly for caching purposes "
  lastPriceUSD: BigDecimal

  " Optional field to track the block number of the last token price "
  lastPriceBlockNumber: BigInt
}

type LiquidityPool @entity {
  " Smart contract address of the pool "
  id: Bytes!

  " The protocol this pool belongs to "
  protocol: DexAmmProtocol!

  " Name of liquidity pool (e.g. Curve.fi DAI/USDC/USDT) "
  name: String

  " Symbol of liquidity pool (e.g. 3CRV) "
  symbol: String

  " Token that is to represent ownership of liquidity "
  liquidityToken: Token

  " Type of token used to track liquidity "
  liquidityTokenType: TokenType

  " Tokens that need to be deposited to take a position in protocol. e.g. WETH and USDC to deposit into the WETH-USDC pool. Array to account for multi-asset pools like Curve and Balancer "
  inputTokens: [Token!]!

  " Additional tokens that are given as reward for position in a protocol, usually in liquidity mining programs. e.g. SUSHI in the Onsen program, MATIC for Aave Polygon, usually in liquidity mining programs. e.g. SUSHI in the Onsen program, MATIC for Aave Polygon "
  rewardTokens: [RewardToken!]

  " Fees per trade incurred to the user. Should include all fees that apply to a pool (e.g. Curve has a trading fee AND an admin fee, which is a portion of the trading fee. Uniswap only has a trading fee and no protocol fee. ) "
  fees: [LiquidityPoolFee!]!

  " Whether this pool is single-sided (e.g. Bancor, Platypus's Alternative Pool). The specifics of the implementation depends on the protocol. "
  isSingleSided: Boolean!

  " Creation timestamp "
  createdTimestamp: BigInt!

  " Creation block number "
  createdBlockNumber: BigInt!

  ##### Quantitative Data #####

  " Current tick representing the price of token0/token1 "
  tick: BigInt

  " Current TVL (Total Value Locked) of this pool in USD "
  totalValueLockedUSD: BigDecimal!

  " The sum of all active and non-active liquidity for this pool. "
  totalLiquidity: BigInt!

  " The sum of all active and non-active liquidity in USD for this pool. "
  totalLiquidityUSD: BigDecimal!

  " All liquidity `k` that is active. Will be equal to totalLiquidity except for in concentrated liquidity - where activeLiquidity is all liquidity positions that contain the pools current tick. "
  activeLiquidity: BigInt!

  " All liquidity in USD that is active. Will be equal to totalLiquidity except for in concentrated liquidity - where activeLiquidity is all liquidity positions that contain the pools current tick. "
  activeLiquidityUSD: BigDecimal!

  " All protocol-side value locked in token amounts that remains uncollected and unused in the pool. "
  uncollectedProtocolSideTokenAmounts: [BigInt!]!

  " All protocol-side value locking in USD that remains uncollected and unused in the pool. "
  uncollectedProtocolSideValuesUSD: [BigDecimal!]!

  " All supply-side value locked in token amounts that remains uncollected and unused in the pool. "
  uncollectedSupplySideTokenAmounts: [BigInt!]!

  " All supply-side value locked in USD that remains uncollected and unused in the pool. "
  uncollectedSupplySideValuesUSD: [BigDecimal!]!

  " All revenue generated by the liquidity pool, accrued to the supply side. "
  cumulativeSupplySideRevenueUSD: BigDecimal!

  " All revenue generated by the liquidity pool, accrued to the protocol. "
  cumulativeProtocolSideRevenueUSD: BigDecimal!

  " All revenue generated by the liquidity pool. "
  cumulativeTotalRevenueUSD: BigDecimal!

  " All trade volume occurred for a specific input token, in native amount. The ordering should be the same as the pool's `inputTokens` field. "
  cumulativeVolumeTokenAmounts: [BigInt!]!

  " All trade volume occurred for a specific input token, in USD. The ordering should be the same as the pool's `inputTokens` field. "
  cumulativeVolumesUSD: [BigDecimal!]!

  " All historical trade volume occurred in this pool, in USD "
  cumulativeVolumeUSD: BigDecimal!

  " Amount of input tokens in the pool. The ordering should be the same as the pool's `inputTokens` field. "
  inputTokenBalances: [BigInt!]!

  " Amount of input tokens in USD in the pool. The ordering should be the same as the pool's `inputTokens` field. "
  inputTokenBalancesUSD: [BigDecimal!]!

  " Weights of input tokens in the liquidity pool in percentage values. For example, 50/50 for Uniswap pools, 48.2/51.8 for a Curve pool, 10/10/80 for a Balancer pool "
  inputTokenWeights: [BigDecimal!]!

  " Total supply of output tokens that are staked (usually in the MasterChef contract). Used to calculate reward APY. "
  stakedOutputTokenAmount: BigInt

  " Per-block reward token emission as of the current block normalized to a day, in token's native amount. This should be ideally calculated as the theoretical rate instead of the realized amount. "
  rewardTokenEmissionsAmount: [BigInt!]

  " Per-block reward token emission as of the current block normalized to a day, in USD value. This should be ideally calculated as the theoretical rate instead of the realized amount. "
  rewardTokenEmissionsUSD: [BigDecimal!]

  " Total number of deposits (add liquidity) "
  cumulativeDepositCount: Int!

  " Total number of withdrawals (remove liquidity) "
  cumulativeWithdrawCount: Int!

  " Total number of trades (swaps) "
  cumulativeSwapCount: Int!

  ##### Account/Position Data #####

  " All positions in this market "
  positions: [Position!]! @derivedFrom(field: "pool")

  " Number of positions in this market "
  positionCount: Int!

  " Number of open positions in this market "
  openPositionCount: Int!

  " Number of closed positions in this market "
  closedPositionCount: Int!

  " Day ID of the most recent daily snapshot "
  lastSnapshotDayID: Int!

  " Hour ID of the most recent hourly snapshot "
  lastSnapshotHourID: Int!

  " Timestamp of the last time this entity was updated "
  lastUpdateTimestamp: BigInt!

  " Block number of the last time this entity was updated "
  lastUpdateBlockNumber: BigInt!

  ##### Snapshots #####

  " Liquidity pool daily snapshots "
  dailySnapshots: [LiquidityPoolDailySnapshot!]! @derivedFrom(field: "pool")

  " Liquidity pool hourly snapshots "
  hourlySnapshots: [LiquidityPoolHourlySnapshot!]! @derivedFrom(field: "pool")

  ##### Events #####

  " All deposit (add liquidity) events occurred in this pool "
  deposits: [Deposit!]! @derivedFrom(field: "pool")

  " All withdraw (remove liquidity) events occurred in this pool "
  withdraws: [Withdraw!]! @derivedFrom(field: "pool")

  " All trade (swap) events occurred in this pool "
  swaps: [Swap!]! @derivedFrom(field: "pool")

  _totalAmountWithdrawn: [BigInt!]!

  _totalAmountCollected: [BigInt!]!

  _totalAmountEarned: [BigInt!]!
}

type DexAmmProtocol implements Protocol @entity {
  " Smart contract address of the protocol's main contract (Factory, Registry, etc) "
  id: Bytes!

  " Name of the protocol, including version. e.g. Uniswap v3 "
  name: String!

  " Slug of protocol, including version. e.g. uniswap-v3 "
  slug: String!

  " Version of the subgraph schema, in SemVer format (e.g. 1.0.0) "
  schemaVersion: String!

  " Version of the subgraph implementation, in SemVer format (e.g. 1.0.0) "
  subgraphVersion: String!

  " Version of the methodology used to compute metrics, loosely based on SemVer format (e.g. 1.0.0) "
  methodologyVersion: String!

  " The blockchain network this subgraph is indexing on "
  network: Network!

  " The type of protocol (e.g. DEX, Lending, Yield, etc) "
  type: ProtocolType!

  ##### Quantitative Data #####

  " Current TVL (Total Value Locked) of the entire protocol "
  totalValueLockedUSD: BigDecimal!

  " The sum of all active and non-active liquidity in USD for this pool. "
  totalLiquidityUSD: BigDecimal!

  " All liquidity in USD that is active. Will be equal to totalLiquidity except for in concentrated liquidity - where activeLiquidity is all liquidity positions that contain the pools current tick. "
  activeLiquidityUSD: BigDecimal!

  " All protocol-side value locking in USD that remains uncollected and unused in the protocol. "
  uncollectedProtocolSideValueUSD: BigDecimal!

  " All supply-side value locking in USD that remains uncollected and unused in the protocol. "
  uncollectedSupplySideValueUSD: BigDecimal!

  " Current PCV (Protocol Controlled Value). Only relevant for protocols with PCV. "
  protocolControlledValueUSD: BigDecimal

  " All historical volume in USD "
  cumulativeVolumeUSD: BigDecimal!

  " Revenue claimed by suppliers to the protocol. LPs on DEXs (e.g. 0.25% of the swap fee in Sushiswap). Depositors on Lending Protocols. NFT sellers on OpenSea. "
  cumulativeSupplySideRevenueUSD: BigDecimal!

  " Gross revenue for the protocol (revenue claimed by protocol). Examples: AMM protocol fee (Sushi’s 0.05%). OpenSea 10% sell fee. "
  cumulativeProtocolSideRevenueUSD: BigDecimal!

  " All revenue generated by the protocol. e.g. 0.30% of swap fee in Sushiswap, all yield generated by Yearn. "
  cumulativeTotalRevenueUSD: BigDecimal!

  " Number of cumulative unique users "
  cumulativeUniqueUsers: Int!

  " Number of cumulative liquidity providers "
  cumulativeUniqueLPs: Int!

  " Number of cumulative traders "
  cumulativeUniqueTraders: Int!

  " Total number of pools "
  totalPoolCount: Int!

  " Total number of open positions "
  openPositionCount: Int!

  " Total number of positions (open and closed) "
  cumulativePositionCount: Int!

  " Day ID of the most recent daily snapshot "
  lastSnapshotDayID: Int!

  " Timestamp of the last time this entity was updated "
  lastUpdateTimestamp: BigInt!

  " Block number of the last time this entity was updated "
  lastUpdateBlockNumber: BigInt!

  ##### Snapshots #####

  " Daily usage metrics for this protocol "
  dailyUsageMetrics: [UsageMetricsDailySnapshot!]!
    @derivedFrom(field: "protocol")

  " Hourly usage metrics for this protocol "
  hourlyUsageMetrics: [UsageMetricsHourlySnapshot!]!
    @derivedFrom(field: "protocol")

  " Daily financial metrics for this protocol "
  financialMetrics: [FinancialsDailySnapshot!]! @derivedFrom(field: "protocol")

  ##### Pools #####

  " All pools that belong to this protocol "
  pools: [LiquidityPool!]! @derivedFrom(field: "protocol")

  " This is a boolean to indicate whether or not the pools have been instantiated the were initialized before Optimism regenesis "
  _regenesis: Boolean!
}
''',
    'balancer': '''type Balancer @entity {
    id: ID!
    color: String!                                      # Bronze, Silver, Gold
    poolCount: Int!                                     # Number of pools
    finalizedPoolCount: Int!                            # Number of finalized pools
    crpCount: Int!                                      # Number of CRP
    pools: [Pool!] @derivedFrom(field: "factoryID")
    txCount: BigInt!                                    # Number of txs
    totalLiquidity: BigDecimal!                         # All the pools liquidity value in USD
    totalSwapVolume: BigDecimal!                        # All the swap volume in USD
    totalSwapFee: BigDecimal!                           # All the swap fee in USD
}

type Pool @entity {
    id: ID!                                             # Pool address
    controller: Bytes!                                  # Controller address
    publicSwap: Boolean!                                # isPublicSwap
    finalized: Boolean!                                 # isFinalized
    crp: Boolean!                                       # Is configurable rights pool
    crpController: Bytes                                # CRP controller address
    symbol: String                                      # Pool token symbol
    name: String                                        # Pool token name
    rights: [String!]!                                  # List of rights (for CRP)
    cap: BigInt                                         # Maximum supply if any (for CRP)
    active: Boolean!                                    # isActive
    swapFee: BigDecimal!                                # Swap Fees
    totalWeight: BigDecimal!
    totalShares: BigDecimal!                            # Total pool token shares
    totalSwapVolume: BigDecimal!                        # Total swap volume in USD
    totalSwapFee: BigDecimal!                           # Total swap fee in USD
    liquidity: BigDecimal!                              # Pool liquidity value in USD
    tokensList: [Bytes!]!                               # Temp workaround until graph supports filtering on derived field
    tokens: [PoolToken!] @derivedFrom(field: "poolId")
    shares: [PoolShare!] @derivedFrom(field: "poolId")
    createTime: Int!                                    # Block time pool was created
    tokensCount: BigInt!                                # Number of tokens in the pool
    holdersCount: BigInt!                               # Number of addresses holding a positive balance of BPT
    joinsCount: BigInt!                                 # liquidity has been added
    exitsCount: BigInt!                                 # liquidity has been removed
    swapsCount: BigInt!
    factoryID: Balancer!
    tx: Bytes                                           # Pool creation transaction id
    swaps: [Swap!] @derivedFrom(field: "poolAddress")
}

type PoolToken @entity {
    id: ID!                                             # poolId + token address
    poolId: Pool!
    symbol: String
    name: String
    decimals: Int!
    address: String!
    balance: BigDecimal!
    denormWeight: BigDecimal!
}

type PoolShare @entity {
    id: ID!                                             # poolId + userAddress
    userAddress: User!
    poolId: Pool!
    balance: BigDecimal!
}

type User @entity {
    id: ID!
    sharesOwned: [PoolShare!]  @derivedFrom(field: "userAddress")
    txs: [Transaction!]  @derivedFrom(field: "userAddress")
    swaps: [Swap!]  @derivedFrom(field: "userAddress")
}

type Swap @entity {
    id: ID!                                 #
    caller: Bytes!                          #
    tokenIn: Bytes!                         #
    tokenInSym: String!                     #
    tokenOut: Bytes!                        #
    tokenOutSym: String!                    #
    tokenAmountIn: BigDecimal!              #
    tokenAmountOut: BigDecimal!             #
    poolAddress: Pool
    userAddress: User                       # User address that initiates the swap
    value: BigDecimal!                      # Swap value in USD
    feeValue: BigDecimal!                   # Swap fee value in USD
    poolTotalSwapVolume: BigDecimal!        # Total pool swap volume in USD
    poolTotalSwapFee: BigDecimal!           # Total pool swap fee in USD
    poolLiquidity: BigDecimal!              # Pool liquidity value in USD
    timestamp: Int!
}

type Transaction @entity {
    id: ID!                         # Log ID
    tx: Bytes!
    event: String
    block: Int!
    timestamp: Int!
    gasUsed: BigDecimal!
    gasPrice: BigDecimal!
    poolAddress: Pool
    userAddress: User
    action: SwapType
    sender: Bytes
}

type TokenPrice @entity {
    id: ID!
    symbol: String
    name: String
    decimals: Int!
    price: BigDecimal!
    poolLiquidity: BigDecimal!
    poolTokenId: String
}

enum SwapType {
    swapExactAmountIn,
    swapExactAmountOut,
    joinswapExternAmountIn,
    joinswapPoolAmountOut,
    exitswapPoolAmountIn,
    exitswapExternAmountOut
}''',
    'decentraland': '''# thegraph doesn't support count operations, but we need them to paginate results
# This entity is a workaround to this issue, but it's still not enough, as we'd need counts for more complex queries
type Count @entity {
  id: ID!

  orderTotal: Int!
  orderParcel: Int!
  orderEstate: Int!
  orderWearable: Int!
  orderENS: Int!
  parcelTotal: Int!
  estateTotal: Int!
  wearableTotal: Int!
  ensTotal: Int!
  started: Int!
  salesTotal: Int!
  salesManaTotal: BigInt!
  creatorEarningsManaTotal: BigInt!
  daoEarningsManaTotal: BigInt!
}

# ---------------------------------------------------------
# Orders --------------------------------------------------
# ---------------------------------------------------------

# thegraph doesn't support nested property searches, so we're doing promoting properties
# we need from each NFT type to the Order, in order to search for them, prefixing them with search_[nft]_[prop]
type Order @entity {
  id: ID!
  marketplaceAddress: Bytes!
  category: Category!
  nft: NFT
  nftAddress: Bytes!
  tokenId: BigInt!
  txHash: Bytes!
  owner: Bytes!
  buyer: Bytes
  price: BigInt!
  status: OrderStatus!
  blockNumber: BigInt!
  expiresAt: BigInt!
  createdAt: BigInt!
  updatedAt: BigInt!
}

# ---------------------------------------------------------
# Bids ----------------------------------------------------
# ---------------------------------------------------------

type Bid @entity {
  id: ID!
  bidAddress: Bytes!
  category: Category!
  nft: NFT
  nftAddress: Bytes!
  tokenId: BigInt!
  bidder: Bytes
  seller: Bytes
  price: BigInt!
  fingerprint: Bytes
  status: OrderStatus!
  blockchainId: String!
  blockNumber: BigInt!
  expiresAt: BigInt!
  createdAt: BigInt!
  updatedAt: BigInt!
}

# ---------------------------------------------------------
# NFTs ----------------------------------------------------
# ---------------------------------------------------------

# aka LAND
type Parcel @entity {
  id: ID!
  tokenId: BigInt!
  owner: Account!
  x: BigInt!
  y: BigInt!
  estate: Estate
  data: Data
  rawData: String
  nft: NFT @derivedFrom(field: "parcel")
}

type Estate @entity {
  id: ID!
  tokenId: BigInt!
  owner: Account!
  parcels: [Parcel!]! @derivedFrom(field: "estate")
  parcelDistances: [Int!]
  adjacentToRoadCount: Int
  size: Int
  data: Data
  rawData: String
  nft: NFT @derivedFrom(field: "estate")
}

type Data @entity {
  id: ID!
  parcel: Parcel
  estate: Estate
  version: String!
  name: String
  description: String
  ipns: String
}

type Wearable @entity {
  id: ID!
  owner: Account!
  representationId: String!
  collection: String!
  name: String!
  description: String!
  category: WearableCategory!
  rarity: WearableRarity!
  bodyShapes: [WearableBodyShape!]
  nft: NFT @derivedFrom(field: "wearable")
}

type ENS @entity {
  id: ID!
  tokenId: BigInt!
  owner: Account!
  caller: Bytes
  beneficiary: Bytes
  labelHash: Bytes
  subdomain: String
  createdAt: BigInt
  nft: NFT @derivedFrom(field: "ens")
}

type NFT @entity {
  id: ID!
  tokenId: BigInt!
  contractAddress: Bytes!
  category: Category!
  owner: Account!
  tokenURI: String

  orders: [Order!] @derivedFrom(field: "nft") # History of all orders. Should only ever be ONE open order. all others must be cancelled or sold
  bids: [Bid!] @derivedFrom(field: "nft") # History of all bids.
  activeOrder: Order

  name: String
  image: String

  parcel: Parcel
  estate: Estate
  wearable: Wearable
  ens: ENS

  createdAt: BigInt!
  updatedAt: BigInt!
  soldAt: BigInt
  transferredAt: BigInt!

  # analytics
  sales: Int!
  volume: BigInt!

  # search indexes
  searchOrderStatus: OrderStatus
  searchOrderPrice: BigInt
  searchOrderExpiresAt: BigInt
  searchOrderCreatedAt: BigInt

  searchIsLand: Boolean

  searchText: String

  searchParcelIsInBounds: Boolean
  searchParcelX: BigInt
  searchParcelY: BigInt
  searchParcelEstateId: String
  searchDistanceToPlaza: Int
  searchAdjacentToRoad: Boolean

  searchEstateSize: Int

  searchIsWearableHead: Boolean
  searchIsWearableAccessory: Boolean
  searchWearableRarity: String # We're using String instead of WearableRarity here so we can later query this field via ()_in
  searchWearableCategory: WearableCategory
  searchWearableBodyShapes: [WearableBodyShape!]
}

# ---------------------------------------------------------
# Account (user) -------------------------------------------
# ---------------------------------------------------------

type Account @entity {
  id: ID! # ETH addr
  address: Bytes!
  nfts: [NFT!] @derivedFrom(field: "owner")
  # analytics
  sales: Int!
  purchases: Int!
  spent: BigInt!
  earned: BigInt!
}

# ---------------------------------------------------------
# Enums ---------------------------------------------------
# ---------------------------------------------------------

enum Category @entity {
  parcel
  estate
  wearable
  ens
}

enum OrderStatus @entity {
  open
  sold
  cancelled
}

enum WearableCategory @entity {
  eyebrows
  eyes
  facial_hair
  hair
  mouth
  upper_body
  lower_body
  feet
  earring
  eyewear
  hat
  helmet
  mask
  tiara
  top_head
  skin
}

enum WearableRarity @entity {
  common
  uncommon
  rare
  epic
  legendary
  mythic
  unique
}

enum WearableBodyShape @entity {
  BaseFemale
  BaseMale
}

# ---------------------------------------------------------
# Sales ---------------------------------------------------
# ---------------------------------------------------------

# We only track sales from Decentraland's smart contracts

enum SaleType @entity {
  bid
  order
}

type Sale @entity {
  id: ID!
  type: SaleType!
  buyer: Bytes!
  seller: Bytes!
  price: BigInt!
  nft: NFT!
  timestamp: BigInt!
  txHash: Bytes!

  # search
  searchTokenId: BigInt!
  searchContractAddress: Bytes!
  searchCategory: String!
}

# Data accumulated and condensed into day stats for all of the Marketplace activity
type AnalyticsDayData @entity {
  id: ID! # timestamp rounded to current day by dividing by 86400
  date: Int!
  sales: Int!
  volume: BigInt!
  creatorsEarnings: BigInt!
  daoEarnings: BigInt!
}''',
    'aave' : '''type Protocol @entity {
  # just 1 for now
  id: ID!
  pools: [Pool!]! @derivedFrom(field: "protocol")
}

# service entity, when we receiving an event we should wknow which pool is it
type ContractToPoolMapping @entity {
  # contract address
  id: ID!
  pool: Pool!
}

type Pool @entity {
  id: ID!
  addressProviderId: BigInt!
  protocol: Protocol!
  pool: Bytes
  poolCollateralManager: Bytes
  poolConfiguratorImpl: Bytes
  poolImpl: Bytes
  poolConfigurator: Bytes
  proxyPriceProvider: Bytes
  lastUpdateTimestamp: Int!

  bridgeProtocolFee: BigInt
  flashloanPremiumTotal: BigInt
  flashloanPremiumToProtocol: BigInt

  reserves: [Reserve!]! @derivedFrom(field: "pool")
  supplyHistory: [Supply!]! @derivedFrom(field: "pool")
  mintUnbackedHistory: [MintUnbacked!]! @derivedFrom(field: "pool")
  backUnbackedHistory: [BackUnbacked!]! @derivedFrom(field: "pool")
  mintedToTreasuryHistory: [MintedToTreasury!]! @derivedFrom(field: "pool")
  isolationModeTotalDebtUpdatedHistory: [IsolationModeTotalDebtUpdated!]!
    @derivedFrom(field: "pool")
  redeemUnderlyingHistory: [RedeemUnderlying!]! @derivedFrom(field: "pool")
  borrowHistory: [Borrow!]! @derivedFrom(field: "pool")
  swapHistory: [SwapBorrowRate!]! @derivedFrom(field: "pool")
  usageAsCollateralHistory: [UsageAsCollateral!]! @derivedFrom(field: "pool")
  rebalanceStableBorrowRateHistory: [RebalanceStableBorrowRate!]! @derivedFrom(field: "pool")
  repayHistory: [Repay!]! @derivedFrom(field: "pool")
  flashLoanHistory: [FlashLoan!]! @derivedFrom(field: "pool")
  liquidationCallHistory: [LiquidationCall!]! @derivedFrom(field: "pool")
  active: Boolean!
  paused: Boolean!
}


interface UserTransaction {
  id: ID!
  txHash: Bytes!
  action: Action!
  pool: Pool!
  user: User!
  timestamp: Int!
}

type Supply implements UserTransaction @entity {
  """
  tx hash
  """
  id: ID!
  txHash: Bytes!
  action: Action!
  pool: Pool!
  user: User!
  caller: User!
  reserve: Reserve!
  referrer: Referrer
  userReserve: UserReserve!
  amount: BigInt!
  timestamp: Int!
  assetPriceUSD: BigDecimal!
}

type SwapBorrowRate implements UserTransaction @entity {
  """
  tx hash
  """
  id: ID!
  txHash: Bytes!
  action: Action!
  pool: Pool!
  user: User!
  reserve: Reserve!
  userReserve: UserReserve!
  borrowRateModeFrom: Int!
  borrowRateModeTo: Int!
  stableBorrowRate: BigInt!
  variableBorrowRate: BigInt!
  timestamp: Int!
}

type Repay implements UserTransaction @entity {
  """
  tx hash
  """
  id: ID!
  txHash: Bytes!
  action: Action!
  pool: Pool!
  user: User!
  repayer: User!
  reserve: Reserve!
  userReserve: UserReserve!
  amount: BigInt!
  timestamp: Int!
  useATokens: Boolean!
  assetPriceUSD: BigDecimal!
}

type FlashLoan @entity {
  """
  tx hash
  """ #
  id: ID!
  pool: Pool!
  reserve: Reserve!
  target: Bytes!
  amount: BigInt!
  totalFee: BigInt!
  lpFee: BigInt!
  protocolFee: BigInt!
  #protocolFee: BigInt!
  initiator: User!
  timestamp: Int!
}

type LiquidationCall implements UserTransaction @entity {
  """
  tx hash
  """ #
  id: ID!
  txHash: Bytes!
  action: Action!
  pool: Pool!
  user: User!
  collateralReserve: Reserve!
  collateralUserReserve: UserReserve!
  collateralAmount: BigInt!
  principalReserve: Reserve!
  principalUserReserve: UserReserve!
  principalAmount: BigInt!
  liquidator: Bytes!
  timestamp: Int!
  collateralAssetPriceUSD: BigDecimal!
  borrowAssetPriceUSD: BigDecimal!
}

type UserReward @entity {
  """
  id: ic:asset:reward:user
  """
  id: ID!
  user: User!
  index: BigInt!
  reward: Reward!
  createdAt: Int!
  updatedAt: Int!
}

type User @entity {
  """
  user address
  """
  id: ID!
  borrowedReservesCount: Int!

  #rewards
  unclaimedRewards: BigInt!
  lifetimeRewards: BigInt!
  rewardsLastUpdated: Int!
  rewards: [UserReward!]! @derivedFrom(field: "user")

  #emode
  eModeCategoryId: EModeCategory

  reserves: [UserReserve!]! @derivedFrom(field: "user")
  supplyHistory: [Supply!]! @derivedFrom(field: "user")
  mintUnbackedHistory: [MintUnbacked!]! @derivedFrom(field: "user")
  backUnbackedHistory: [BackUnbacked!]! @derivedFrom(field: "backer")
  userEmodeSetHistory: [UserEModeSet!]! @derivedFrom(field: "user")
  redeemUnderlyingHistory: [RedeemUnderlying!]! @derivedFrom(field: "user")
  usageAsCollateralHistory: [UsageAsCollateral!]! @derivedFrom(field: "user")
  borrowHistory: [Borrow!]! @derivedFrom(field: "user")
  swapHistory: [SwapBorrowRate!]! @derivedFrom(field: "user")
  rebalanceStableBorrowRateHistory: [RebalanceStableBorrowRate!]! @derivedFrom(field: "user")
  repayHistory: [Repay!]! @derivedFrom(field: "user")
  liquidationCallHistory: [LiquidationCall!]! @derivedFrom(field: "user")
  rewardedActions: [RewardedAction!]! @derivedFrom(field: "user")
  claimRewards: [ClaimRewardsCall!]! @derivedFrom(field: "user")
}

type SwapHistory @entity {
  """
  tx hash
  """
  id: ID!
  fromAsset: String!
  toAsset: String!
  fromAmount: BigInt!
  receivedAmount: BigInt!
  swapType: String!
}''',
  
}
