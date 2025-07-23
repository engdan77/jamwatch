from .log import logger
from jamwatch.app_types import FilterDistributionStat, File


def b2mb(bytes_: int) -> int:
    return int(bytes_ / 1024 / 1024)


def mb2b(mb: int) -> int:
    return mb * 1024 * 1024


def filter_files(filter_distribution: list[FilterDistributionStat], files_list: list[File], max_mb: int = 128) -> list[File]:
    """
    Filters a list of files based on the given filter distribution and limits the total file size.
    The function iterates over the provided filter distribution sorted by descending order of
    percentages and selects files that match the specified filter. The size of selected files
    is capped based on the percentage and the maximum size limit provided.

    :param filter_distribution: A list of filter distribution statistics, each containing a filter
        and its associated percentage for allocation.
    :param files_list: A list of files where each file contains metadata such as track and size.
    :param max_mb: Optional maximum size in megabytes of the files that should be filtered,
        defaults to 128 MB.
    :return: A filtered list of files that match the given filter distribution
        and fall within the size constraints.
    """
    output: list[File] = []
    descending_filter_distribution = sorted(filter_distribution, key=lambda x: x.percentage, reverse=True)
    if sum(_.percentage for _ in descending_filter_distribution) > 100:
        logger.warning("Filter distribution percentage is greater than 100")
    if sum(_['size'] for _ in files_list) < mb2b(max_mb):
        logger.warning(f"Less than {max_mb} MB of files to filter so % may be inaccurate")
    for filter_stat in descending_filter_distribution:
        current_bytes_filled = 0
        max_bytes = mb2b(int(max_mb * 0.9 * (filter_stat.percentage / 100)))  # Make it 90% to leave some margins
        for file in files_list:
            track = file['track']
            if track.contains(filter_stat.filter):
                current_bytes_filled += file['size']
                output.append(file)
                if current_bytes_filled > max_bytes:
                    logger.info(f"Filled {b2mb(current_bytes_filled)} MB ({filter_stat.filter}) with {filter_stat.percentage}%")
                    break
    return output
