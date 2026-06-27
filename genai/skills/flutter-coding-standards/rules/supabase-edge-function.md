---
title: Edge Function Invocation
impact: HIGH
impactDescription: Edge Function の呼び出し方法
tags: flutter, supabase, edge-function, api
---

## Edge Function Invocation

Flutter から Supabase Edge Function を呼び出す方法です。

**GET リクエスト（データ取得）：**

```dart
Future<List<Schedule>> getTodaySchedules(String userId) async {
  final supabase = Supabase.instance.client;
  final session = supabase.auth.currentSession;

  if (session == null) {
    throw Exception('認証が必要です');
  }

  final queryParams = {
    'userId': userId,
    'todayStart': DateTime.now().toIso8601String(),
  };

  final response = await supabase.functions.invoke(
    'get-today-schedules',
    method: HttpMethod.get,
    queryParameters: queryParams,
  );

  if (response.status != 200) {
    throw Exception('スケジュールの取得に失敗しました');
  }

  final data = response.data as Map<String, dynamic>;
  if (data['success'] != true) {
    throw Exception(data['error'] ?? 'Unknown error');
  }

  final schedules = (data['data'] as List)
      .map((e) => ScheduleModel.fromJson(e).toEntity())
      .toList();

  return schedules;
}
```

**POST リクエスト（データ作成・更新）：**

```dart
Future<void> createOrder(OrderInput input) async {
  final supabase = Supabase.instance.client;
  final session = supabase.auth.currentSession;

  if (session == null) {
    throw Exception('認証が必要です');
  }

  final response = await supabase.functions.invoke(
    'create-order',
    method: HttpMethod.post,
    body: input.toJson(),
  );

  if (response.status != 200 && response.status != 201) {
    throw Exception('注文の作成に失敗しました');
  }

  final data = response.data as Map<String, dynamic>;
  if (data['success'] != true) {
    throw Exception(data['error'] ?? 'Unknown error');
  }
}
```

**DataSource での実装例：**

```dart
class OrderRemoteDataSourceImpl implements OrderRemoteDataSource {
  final SupabaseClient _supabase;

  OrderRemoteDataSourceImpl(this._supabase);

  @override
  Future<List<OrderModel>> getOrders(String userId) async {
    final response = await _supabase.functions.invoke(
      'get-orders',
      method: HttpMethod.get,
      queryParameters: {'userId': userId},
    );

    _validateResponse(response, 'get-orders');

    final data = response.data as Map<String, dynamic>;
    return (data['data'] as List)
        .map((e) => OrderModel.fromJson(e))
        .toList();
  }

  void _validateResponse(FunctionResponse response, String functionName) {
    if (response.status != 200) {
      throw ServerException(
        '$functionName failed with status ${response.status}',
        statusCode: response.status,
      );
    }

    final data = response.data as Map<String, dynamic>;
    if (data['success'] != true) {
      throw ServerException(data['error'] ?? 'Unknown error');
    }
  }
}
```

**HTTP メソッドの使い分け：**

| メソッド | 用途 |
|----------|------|
| `HttpMethod.get` | データ取得 |
| `HttpMethod.post` | データ作成 |
| `HttpMethod.put` | **禁止**（全体更新は使わず、PATCH で部分更新する） |
| `HttpMethod.patch` | データ更新（部分） |
| `HttpMethod.delete` | データ削除 |

- **GET**: 一覧取得・単体取得・検索・エクスポートなど、副作用のない読み取り。クエリパラメータで条件を渡す。
- **POST**: 新規リソースの作成（登録・申込・送信）、冪等でない操作、複雑な条件付きの作成。
- **PATCH**: 既存リソースの部分更新。変更したいフィールドだけ送り、全体を送らない。プロフィール更新・設定変更・ステータス変更など。
- **DELETE**: リソースの削除。論理削除の場合は「削除リクエストを送る」役割として使用。

**チェックリスト：**

- [ ] 認証状態（session）を確認
- [ ] 適切な HTTP メソッドを使用
- [ ] レスポンスのステータスコードをチェック
- [ ] `success` フラグをチェック
- [ ] エラーハンドリングを実装
- [ ] Model への変換を実装
