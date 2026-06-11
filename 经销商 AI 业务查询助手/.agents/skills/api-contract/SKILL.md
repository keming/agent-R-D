---
name: api-contract
description: API Contract Agent. OpenAPI 스펙 정의, Mock Server 생성, Contract-First 개발을 담당합니다. Frontend/Backend 간 API 계약을 관리합니다.
allowed-tools: Bash(npm:*, npx:*), Read, Write, Edit, Grep, Glob
---

# API Contract Agent

## 역할

Contract-First 개발을 위한 API 계약(OpenAPI 스펙) 정의 및 관리를 담당합니다.

## Contract-First 원칙

```
┌─────────────────────────────────────────────────────────────────┐
│                    Contract-First 개발 흐름                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. API 계약 정의 (OpenAPI 3.0)                                  │
│           │                                                     │
│           ▼                                                     │
│  2. 계약 검증 및 합의 (Frontend ↔ Backend)                        │
│           │                                                     │
│           ├──────────────┬──────────────┐                       │
│           ▼              ▼              ▼                       │
│  3-A. Mock Server   3-B. Frontend    3-C. Backend              │
│       생성              개발 시작        개발 시작               │
│                         (Mock 사용)     (스펙 준수)              │
│           │              │              │                       │
│           └──────────────┴──────────────┘                       │
│                          │                                      │
│                          ▼                                      │
│  4. Contract Test로 검증                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## OpenAPI 스펙 작성

### 기본 구조

```yaml
openapi: 3.0.3
info:
  title: Feature API
  description: 기능 설명
  version: 1.0.0

servers:
  - url: /api/v1
    description: API Server

paths:
  /resource:
    get:
      summary: 리소스 목록 조회
      operationId: getResources
      tags:
        - Resource
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: 성공
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResourceListResponse'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalError'

    post:
      summary: 리소스 생성
      operationId: createResource
      tags:
        - Resource
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateResourceDto'
      responses:
        '201':
          description: 생성됨
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Resource'
        '400':
          $ref: '#/components/responses/ValidationError'
        '401':
          $ref: '#/components/responses/Unauthorized'

components:
  schemas:
    Resource:
      type: object
      required:
        - id
        - name
        - createdAt
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
          minLength: 1
          maxLength: 100
        description:
          type: string
          nullable: true
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time

    CreateResourceDto:
      type: object
      required:
        - name
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
        description:
          type: string
          nullable: true

    ResourceListResponse:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Resource'
        pagination:
          $ref: '#/components/schemas/Pagination'

    Pagination:
      type: object
      properties:
        page:
          type: integer
        limit:
          type: integer
        total:
          type: integer
        totalPages:
          type: integer

    Error:
      type: object
      properties:
        code:
          type: string
        message:
          type: string
        details:
          type: array
          items:
            type: object

  responses:
    Unauthorized:
      description: 인증 실패
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: UNAUTHORIZED
            message: 인증이 필요합니다

    ValidationError:
      description: 유효성 검증 실패
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: VALIDATION_ERROR
            message: 입력값이 올바르지 않습니다

    InternalError:
      description: 서버 오류
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: INTERNAL_ERROR
            message: 서버 오류가 발생했습니다

  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - BearerAuth: []
```

## Mock Server 생성

### Prism (OpenAPI Mock Server)

```bash
# 설치
npm install -g @stoplight/prism-cli

# Mock Server 실행
prism mock api-contract.yaml -p 4010

# 동적 응답 생성
prism mock api-contract.yaml -p 4010 --dynamic
```

### MSW (Mock Service Worker) 핸들러 생성

```typescript
// src/mocks/handlers.ts
import { rest } from 'msw';

export const handlers = [
  // GET /api/v1/resource
  rest.get('/api/v1/resource', (req, res, ctx) => {
    const page = Number(req.url.searchParams.get('page')) || 1;
    const limit = Number(req.url.searchParams.get('limit')) || 20;

    return res(
      ctx.status(200),
      ctx.json({
        data: [
          {
            id: '550e8400-e29b-41d4-a716-446655440000',
            name: 'Sample Resource',
            description: 'Description',
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
          },
        ],
        pagination: {
          page,
          limit,
          total: 1,
          totalPages: 1,
        },
      })
    );
  }),

  // POST /api/v1/resource
  rest.post('/api/v1/resource', async (req, res, ctx) => {
    const body = await req.json();

    if (!body.name) {
      return res(
        ctx.status(400),
        ctx.json({
          code: 'VALIDATION_ERROR',
          message: 'name은 필수입니다',
        })
      );
    }

    return res(
      ctx.status(201),
      ctx.json({
        id: '550e8400-e29b-41d4-a716-446655440001',
        name: body.name,
        description: body.description || null,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      })
    );
  }),
];
```

## Contract Test (Pact)

### Consumer (Frontend) 테스트

```typescript
// consumer.pact.spec.ts
import { PactV3, MatchersV3 } from '@pact-foundation/pact';

const provider = new PactV3({
  consumer: 'Frontend',
  provider: 'Backend',
});

describe('Resource API Contract', () => {
  it('should get resources', async () => {
    await provider
      .given('resources exist')
      .uponReceiving('a request for resources')
      .withRequest({
        method: 'GET',
        path: '/api/v1/resource',
        query: { page: '1', limit: '20' },
      })
      .willRespondWith({
        status: 200,
        body: MatchersV3.like({
          data: MatchersV3.eachLike({
            id: MatchersV3.uuid(),
            name: MatchersV3.string('Sample'),
            createdAt: MatchersV3.datetime(),
          }),
          pagination: {
            page: 1,
            limit: 20,
            total: MatchersV3.integer(),
          },
        }),
      });

    await provider.executeTest(async (mockServer) => {
      const response = await fetch(`${mockServer.url}/api/v1/resource?page=1&limit=20`);
      const data = await response.json();

      expect(data.data).toBeDefined();
      expect(data.pagination).toBeDefined();
    });
  });
});
```

### Provider (Backend) 검증

```typescript
// provider.pact.spec.ts
import { Verifier } from '@pact-foundation/pact';

describe('Pact Verification', () => {
  it('should validate contract', async () => {
    const verifier = new Verifier({
      providerBaseUrl: 'http://localhost:3000',
      pactUrls: ['./pacts/frontend-backend.json'],
      stateHandlers: {
        'resources exist': async () => {
          // 테스트 데이터 준비
        },
      },
    });

    await verifier.verifyProvider();
  });
});
```

## 스펙 검증

```bash
# OpenAPI 스펙 검증
npx @redocly/cli lint api-contract.yaml

# 스펙 변경 감지 (Breaking Changes)
npx @redocly/cli diff old-spec.yaml new-spec.yaml

# 문서 생성
npx @redocly/cli build-docs api-contract.yaml
```

## 타입 생성

```bash
# TypeScript 타입 생성
npx openapi-typescript api-contract.yaml -o src/types/api.d.ts

# API 클라이언트 생성
npx openapi-generator-cli generate -i api-contract.yaml -g typescript-axios -o src/api
```

## 체크리스트

### 스펙 작성 체크리스트
- [ ] 모든 엔드포인트가 정의되었는가?
- [ ] 요청/응답 스키마가 완전한가?
- [ ] 에러 응답이 정의되었는가?
- [ ] 인증 방식이 명시되었는가?
- [ ] 예시가 포함되었는가?

### 계약 합의 체크리스트
- [ ] Frontend 팀이 검토했는가?
- [ ] Backend 팀이 검토했는가?
- [ ] Mock Server가 정상 동작하는가?
- [ ] 에러 케이스가 합의되었는가?

## 산출물 위치

- OpenAPI 스펙: `docs/features/<기능명>/requirements/api-contract.yaml`
- MSW 핸들러: `src/mocks/handlers/<기능명>.ts`
- Pact 계약: `pacts/`
- 생성된 타입: `src/types/api.d.ts`
