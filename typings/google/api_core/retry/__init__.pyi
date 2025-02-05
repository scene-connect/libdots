"""
This type stub file was generated by pyright.
"""

from .retry_base import RetryFailureReason
from .retry_base import build_retry_error
from .retry_base import exponential_sleep_generator
from .retry_base import if_exception_type
from .retry_base import if_transient_error
from .retry_streaming import StreamingRetry
from .retry_streaming import retry_target_stream
from .retry_streaming_async import AsyncStreamingRetry
from .retry_streaming_async import retry_target_stream as retry_target_stream_async
from .retry_unary import Retry
from .retry_unary import retry_target
from .retry_unary_async import AsyncRetry
from .retry_unary_async import retry_target as retry_target_async

"""Retry implementation for Google API client libraries."""
__all__ = ("exponential_sleep_generator", "if_exception_type", "if_transient_error", "build_retry_error", "RetryFailureReason", "Retry", "AsyncRetry", "StreamingRetry", "AsyncStreamingRetry", "retry_target", "retry_target_async", "retry_target_stream", "retry_target_stream_async")
