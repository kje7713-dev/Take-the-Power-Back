# Take the Power Back — Build Roadmap

This roadmap defines a practical, infrastructure-free path to building a usable
file-based social client that conforms to `file-social-v0.1`.

The emphasis is on shipping, not theorizing.

---

## Phase 0 — Foundations & Guardrails

**Goal:** Lock constraints early and prevent scope drift.

### Tasks
- Commit `spec/file-social-v0.1.md`
- Add `spec/CHANGELOG.md`
- Create `spec/examples/` containing:
  - `profile.json`
  - two example posts (text-only, external media)
  - one comment
  - one tombstone
- Add basic JSON linting / formatting rules

### Exit Criteria
- A fresh clone can understand the data model by reading examples alone.

---

## Phase 1 — Read-Only Viewer (MVP)

**Goal:** Prove the model works: folders → timeline.

### Capabilities
- Select/import a User Folder
- Parse `profile.json`
- Read `posts/`
- Sort posts by `created_at` (descending)
- Render text posts and attachments
- Scan `comments/` and attach to posts
- Deduplicate by `id`
- Respect tombstones

### Notes
- No writing yet
- No subscriptions yet
- No sync assumptions

### Exit Criteria
- Point the app at a folder and see a usable chronological timeline.

---

## Phase 2 — Writer (Create / Edit / Delete)

**Goal:** Allow users to create and manage their own content.

### Capabilities
- Compose new posts
- Write valid post JSON into `posts/`
- Attach media:
  - copy local files into `media/`
  - reference external URLs
- Edit posts (rewrite file + set `updated_at`)
- Delete posts via:
  - tombstones (preferred)
  - physical deletion (allowed)

### Exit Criteria
- User can create, edit, and delete posts that render correctly in Phase 1 viewer.

---

## Phase 3 — Manual Social Graph (Subscriptions)

**Goal:** Make it social without centralization.

### Capabilities
- Add a person by importing another User Folder
- Store subscriptions locally (client-owned)
- Aggregate posts across multiple folders
- Apply visibility rules:
  - `private`: owner only
  - `friends`: either-direction subscription
  - `public` / `unlisted`: visible when subscribed
- Mute / unfollow sources
- Optional: toggle auto-loading of external media

### Exit Criteria
- Multi-person feed works entirely offline.

---

## Phase 4 — Hardening & Durability

**Goal:** Survive real-world usage and sync chaos.

### Capabilities
- Robust ID-based deduplication
- Conflict resolution per spec:
  - prefer latest `updated_at`
  - fallback to latest `created_at`
- Incremental scanning (avoid full rescans)
- Index/cache parsed data locally (non-spec)
- External media caching with user control
- Export user folder (ZIP or directory copy)
- Debug screen for ignored/invalid files

### Exit Criteria
- Handles large folders (10k+ posts) without degrading.

---

## Phase 5 — Packaging & Distribution (Optional)

**Goal:** Make it installable and shareable.

### Options
- iOS (Files / iCloud driven)
- macOS (best filesystem access)
- Web (demo-friendly, limited FS access)
- Android

### Capabilities
- Onboarding that never mentions JSON
- "Where your data lives" explanation screen
- Version tagging and releases
- License finalized

### Exit Criteria
- Non-technical users can use the app without guidance.

---

## Recommended Build Order

1. Spec examples
2. Read-only viewer
3. Writer (create/edit/delete)
4. Subscriptions & aggregation
5. Hardening & caching
6. Packaging (if desired)

---

## Default Technical Decisions

These are defaults unless explicitly changed:

- Subscriptions stored locally (not shared files)
- Tombstones preferred for deletions
- External media opt-in caching
- ULIDs for IDs
- Index/cache stored in client local storage

---

## Guiding Principle

If a feature requires:
- a server
- global state
- ranking
- discovery
- engagement optimization

…it does not belong in this project.

Chronology over algorithms.
Ownership over platforms.
Files over feeds.
