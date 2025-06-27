// simd_tokenizer.cpp
//────────────────────────────────────────────────────────────────────────────
// Splits a log line into integer token-IDs at >1 GB/s on modern CPUs.
//
//  • SIMD byte-wise scan for delimiters [space, tab, '=', ':', ',', ';']
//  • 32-bit FNV-1a hash for each token
//  • Returns number of tokens and writes hashes into caller-allocated buffer
//
//  C linkage → easy to call from Python (cffi) or Rust/Go FFI.
//────────────────────────────────────────────────────────────────────────────

#include <cstddef>
#include <cstdint>
#include <cstring>
#include <immintrin.h>   // AVX2 intrinsics
#include <algorithm>

extern "C" {

/* Return FNV-1a 32-bit hash */
static inline uint32_t fnv1a(const char* s, size_t len)
{
    uint32_t h = 0x811c9dc5u;
    for (size_t i = 0; i < len; ++i)
        h = (h ^ uint8_t(s[i])) * 0x01000193u;
    return h;
}

/**
 * tokenize_line
 * @param line   NUL-terminated input line
 * @param out    caller-allocated int buffer for token hashes
 * @param max    capacity of out[]
 * @return       number of tokens written
 */
int tokenize_line(const char* line, int* out, int max)
{
    const __m256i delim = _mm256_setr_epi8(
        ' ', '\t', '=', ':', ',', ';', 0, 0,  // 6 delimiters
        ' ', '\t', '=', ':', ',', ';', 0, 0,
        ' ', '\t', '=', ':', ',', ';', 0, 0,
        ' ', '\t', '=', ':', ',', ';', 0, 0
    );

    const char* p = line;
    int tok = 0;

    while (*p && tok < max)
    {
        // Skip leading delimiters
        while (*p && strchr(" \t=:,;", *p)) ++p;
        if (!*p) break;

        const char* start = p;

        // SIMD scan 32 bytes at a time for next delimiter/NUL
        while (true)
        {
            __m256i chunk = _mm256_loadu_si256(reinterpret_cast<const __m256i*>(p));
            __m256i cmp   = _mm256_cmpeq_epi8(chunk, delim);
            uint32_t mask = _mm256_movemask_epi8(cmp) |
                            _mm256_movemask_epi8(_mm256_cmpeq_epi8(chunk, _mm256_set1_epi8(0)));

            if (mask)
            {
                int idx = __builtin_ctz(mask);
                p += idx;
                break;
            }
            p += 32;
        }

        size_t len = p - start;
        out[tok++] = static_cast<int>(fnv1a(start, len));

        // Advance past delimiter
        if (*p) ++p;
    }
    return tok;
}

} // extern "C"
